#!/usr/bin/env python3
"""Prepare and apply AI-assisted review decisions for local reference papers."""

from __future__ import annotations

import argparse
import hashlib
import json
import re
import shutil
import subprocess
import sys
import unicodedata
from collections import Counter
from dataclasses import asdict, dataclass
from pathlib import Path

from generate_bib_map import write_mapping


REPO_ROOT = Path(__file__).resolve().parent.parent
REF_DIR = REPO_ROOT / "ref_papers"
QUEUE_DIR = REF_DIR / "Analysis"
RELEVANT_DIR = REF_DIR / "Relevant"
NOT_RELATED_DIR = REF_DIR / "NotRelated"
REVIEW_FILE = REF_DIR / "review_queue.json"
BIB_FILE = REPO_ROOT / "aftertext" / "references.bib"
MAP_FILE = REF_DIR / "bib_map.json"

NOISE_PREFIXES = (
    "accepted for publication",
    "article in press",
    "contents lists available",
    "journal homepage",
    "see discussions, stats",
    "invited paper",
    "special section on",
)

STOPWORDS = {
    "a",
    "an",
    "and",
    "approach",
    "based",
    "by",
    "for",
    "from",
    "in",
    "new",
    "of",
    "on",
    "support",
    "the",
    "through",
    "to",
    "using",
    "with",
}


@dataclass(frozen=True)
class BibEntry:
    key: str
    title: str


@dataclass(frozen=True)
class ReviewItem:
    filename: str
    title: str
    author_hint: str
    year: str
    abstract: str
    keywords: list[str]
    suggested_bib_key: str
    bib_key_source: str


def slugify(text: str) -> str:
    text = unicodedata.normalize("NFKD", text)
    text = text.encode("ascii", "ignore").decode("ascii")
    return re.sub(r"[^a-z0-9]+", "", text.lower())


def normalize_title(text: str) -> str:
    text = unicodedata.normalize("NFKD", text)
    text = text.encode("ascii", "ignore").decode("ascii")
    text = text.lower().replace("&", "and")
    text = re.sub(r"[\W_]+", " ", text)
    return " ".join(text.split())


def tokenize(text: str) -> set[str]:
    return {token for token in normalize_title(text).split() if len(token) > 2 and token not in STOPWORDS}


def run_command(*args: str) -> str:
    completed = subprocess.run(args, check=False, capture_output=True, text=True)
    if completed.returncode != 0:
        return ""
    return completed.stdout


def load_bib_entries(path: Path) -> list[BibEntry]:
    content = path.read_text(encoding="utf-8")
    entries: list[BibEntry] = []
    for raw_entry in re.split(r"(?=@[A-Za-z]+{)", content):
        if not raw_entry.strip():
            continue
        key_match = re.match(r"@[A-Za-z]+{([^,]+),", raw_entry)
        title_match = re.search(r"title\s*=\s*[{\"](.+?)[}\"],?\s*$", raw_entry, flags=re.MULTILINE)
        if not key_match or not title_match:
            continue
        title = " ".join(title_match.group(1).split())
        entries.append(BibEntry(key=key_match.group(1).strip(), title=title))
    return entries


def extract_pdf_info(path: Path) -> dict[str, str]:
    info: dict[str, str] = {}
    for line in run_command("pdfinfo", str(path)).splitlines():
        if ":" not in line:
            continue
        key, value = line.split(":", 1)
        info[key.strip()] = value.strip()
    return info


def extract_text(path: Path, pages: int = 2) -> str:
    return run_command("pdftotext", "-f", "1", "-l", str(pages), "-nopgbrk", str(path), "-")


def clean_lines(text: str) -> list[str]:
    lines: list[str] = []
    for line in text.splitlines():
        cleaned = re.sub(r"\s+", " ", line).strip()
        if not cleaned or re.fullmatch(r"\d+", cleaned):
            continue
        lowered = cleaned.lower()
        if lowered.startswith(NOISE_PREFIXES):
            continue
        if lowered.startswith(("doi:", "http", "www.")):
            continue
        if "copyright" in lowered and "ieee" in lowered:
            continue
        lines.append(cleaned)
    return lines


def looks_like_author_line(line: str) -> bool:
    lowered = line.lower()
    if "@" in line:
        return True
    if any(word in lowered for word in ("university", "department", "laboratory", "school of", "institute", "faculty")):
        return True
    technical_terms = ("802.11", "qos", "wlan", "wireless", "v2x", "vehicular", "scheduling", "resource allocation", "tsn")
    if any(term in lowered for term in technical_terms):
        return False
    words = re.findall(r"[A-Za-z][A-Za-z'.-]+", line)
    capitals = sum(1 for word in words if word[:1].isupper())
    return len(words) >= 3 and capitals >= max(2, len(words) - 1) and ("," in line or " and " in lowered or len(words) <= 8)


def extract_title(info: dict[str, str], text: str, path: Path) -> tuple[str, int]:
    meta_title = info.get("Title", "").strip()
    if meta_title and meta_title.lower() != "ieee paper template in a4 (v1)":
        return " ".join(meta_title.split()), 0

    lines = clean_lines(text)
    title_lines: list[str] = []
    consumed = 0
    for line in lines[:14]:
        lowered = line.lower()
        if lowered.startswith(("abstract", "keywords:", "index terms")) and title_lines:
            break
        if looks_like_author_line(line) and title_lines:
            break
        if lowered.startswith(("wireless netw", "computer communications", "journal of ", "ieice trans.", "international journal", "mobile computing", "electronics", "applied sciences", "computers", "sensors")):
            continue
        title_lines.append(line)
        consumed += 1
        if len(title_lines) >= 4 or len(" ".join(title_lines)) > 180:
            break

    title = " ".join(title_lines)
    title = re.sub(r"\s+([,.:;!?])", r"\1", title)
    title = re.sub(r"\s{2,}", " ", title).strip()
    if title:
        return title, consumed
    return path.stem.replace("_", " "), 0


def extract_author_hint(info: dict[str, str], lines: list[str], title_line_count: int, path: Path) -> str:
    meta_author = info.get("Author", "").strip()
    if meta_author:
        return meta_author
    scan = lines[title_line_count:title_line_count + 8] if title_line_count else lines[:12]
    for line in scan:
        if looks_like_author_line(line):
            return line
    return path.stem


def extract_year(info: dict[str, str], text: str) -> str:
    candidates = re.findall(r"\b(19\d{2}|20[0-3]\d)\b", text)
    if candidates:
        preferred = [candidate for candidate in candidates if 2000 <= int(candidate) <= 2030] or candidates
        counts = Counter(preferred)
        return sorted(counts.items(), key=lambda item: (-item[1], int(item[0])))[0][0]
    creation = info.get("CreationDate", "")
    match = re.search(r"(19\d{2}|20[0-3]\d)", creation)
    if match:
        return match.group(1)
    return "0000"


def extract_keywords(text: str) -> list[str]:
    compact = re.sub(r"\s+", " ", text)
    match = re.search(r"(keywords|index terms)\s*[:.-]?\s*(.+?)(?:\s{2,}|1\s+introduction|introduction\b)", compact, flags=re.IGNORECASE)
    if not match:
        return []
    raw = match.group(2)
    parts = [part.strip(" ,;:.") for part in re.split(r"[;,]", raw)]
    return [part for part in parts if part][:10]


def looks_like_heading(line: str) -> bool:
    lowered = line.lower()
    if lowered in {"introduction", "background", "related work", "conclusion"}:
        return True
    if re.match(r"^(\d+|[ivx]+)[.)]?\s+[A-Z]", line):
        return True
    return False


def extract_abstract(lines: list[str], title_line_count: int) -> str:
    abstract_lines: list[str] = []
    start_index = None

    for idx, line in enumerate(lines[:80]):
        lowered = line.lower()
        if lowered == "abstract":
            start_index = idx + 1
            break
        if lowered.startswith("abstract "):
            abstract_lines.append(line.split(" ", 1)[1].strip())
            start_index = idx + 1
            break
        if lowered.startswith("abstract:"):
            abstract_lines.append(line.split(":", 1)[1].strip())
            start_index = idx + 1
            break

    if start_index is None:
        start_index = min(len(lines), title_line_count + 2)

    for line in lines[start_index:start_index + 18]:
        lowered = line.lower()
        if lowered.startswith(("keywords", "index terms")):
            break
        if looks_like_heading(line):
            break
        if looks_like_author_line(line) and not abstract_lines:
            continue
        abstract_lines.append(line)
        if len(" ".join(abstract_lines)) > 1400:
            break

    abstract = " ".join(abstract_lines)
    abstract = re.sub(r"\s{2,}", " ", abstract).strip(" -:")
    return abstract[:1400]


def find_existing_bib_key(title: str, bib_entries: list[BibEntry]) -> str | None:
    norm_title = normalize_title(title)
    title_tokens = tokenize(title)
    best_key = None
    best_score = 0.0

    for entry in bib_entries:
        entry_norm = normalize_title(entry.title)
        if norm_title and norm_title == entry_norm:
            return entry.key
        entry_tokens = tokenize(entry.title)
        if not title_tokens or not entry_tokens:
            continue
        overlap = len(title_tokens & entry_tokens)
        if overlap == 0:
            continue
        score = overlap / len(title_tokens | entry_tokens)
        if score > best_score:
            best_score = score
            best_key = entry.key

    if best_score >= 0.62:
        return best_key
    return None


def generate_bib_key(title: str, author_hint: str, year: str, existing_keys: set[str]) -> str:
    author_segments = [segment.strip() for segment in re.split(r",| and ", author_hint) if segment.strip()]
    first_author = author_segments[0] if author_segments else author_hint
    author_tokens = [token for token in re.findall(r"[A-Za-z][A-Za-z'.-]+", first_author) if token.lower() not in {"and", "et", "al"}]
    author_part = slugify(author_tokens[-1] if author_tokens else "paper")[:16] or "paper"

    keyword = "paper"
    for token in re.findall(r"[A-Za-z0-9+.-]+", title):
        folded = slugify(token)
        if folded and folded not in STOPWORDS and folded != author_part:
            keyword = folded[:24]
            break

    base_key = f"{author_part}{year}{keyword.title()}"
    key = re.sub(r"[^A-Za-z0-9_]", "", base_key) or f"Paper{year}"
    if key not in existing_keys:
        return key

    suffix = 2
    while f"{key}{suffix}" in existing_keys:
        suffix += 1
    return f"{key}{suffix}"


def load_mapping() -> dict[str, str]:
    if not MAP_FILE.exists():
        return {}
    return json.loads(MAP_FILE.read_text(encoding="utf-8"))


def load_review_queue() -> dict[str, object]:
    if not REVIEW_FILE.exists():
        return {"papers": []}
    return json.loads(REVIEW_FILE.read_text(encoding="utf-8"))


def save_review_queue(payload: dict[str, object]) -> None:
    REVIEW_FILE.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")


def build_review_item(path: Path, bib_entries: list[BibEntry], mapping: dict[str, str], existing_keys: set[str]) -> ReviewItem:
    info = extract_pdf_info(path)
    text = extract_text(path, pages=2)
    lines = clean_lines(text)
    title, title_line_count = extract_title(info, text, path)
    author_hint = extract_author_hint(info, lines, title_line_count, path)
    year = extract_year(info, text)
    abstract = extract_abstract(lines, title_line_count)
    keywords = extract_keywords(text)

    if path.name in mapping:
        suggested_key = mapping[path.name]
        key_source = "bib_map.json"
    else:
        existing_key = find_existing_bib_key(title, bib_entries)
        if existing_key:
            suggested_key = existing_key
            key_source = "references.bib"
        else:
            suggested_key = generate_bib_key(title, author_hint, year, existing_keys)
            key_source = "generated"

    existing_keys.add(suggested_key)
    return ReviewItem(
        filename=path.name,
        title=title,
        author_hint=author_hint,
        year=year,
        abstract=abstract,
        keywords=keywords,
        suggested_bib_key=suggested_key,
        bib_key_source=key_source,
    )


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(65536), b""):
            digest.update(chunk)
    return digest.hexdigest()


def resolve_destination(path: Path, target_dir: Path) -> Path:
    destination = target_dir / path.name
    if not destination.exists():
        return destination
    if sha256(destination) == sha256(path):
        path.unlink()
        return destination
    stem = destination.stem
    suffix = destination.suffix
    counter = 2
    while True:
        candidate = target_dir / f"{stem}__{counter}{suffix}"
        if not candidate.exists():
            return candidate
        counter += 1


def iter_queue_pdfs() -> list[Path]:
    REF_DIR.mkdir(exist_ok=True)
    RELEVANT_DIR.mkdir(exist_ok=True)
    NOT_RELATED_DIR.mkdir(exist_ok=True)
    QUEUE_DIR.mkdir(exist_ok=True)
    return sorted(QUEUE_DIR.glob("*.pdf"), key=lambda item: item.name.lower())


def prepare_review_queue() -> int:
    if not BIB_FILE.exists():
        print(f"Missing bibliography file: {BIB_FILE}", file=sys.stderr)
        return 1

    bib_entries = load_bib_entries(BIB_FILE)
    mapping = load_mapping()
    existing_keys = {entry.key for entry in bib_entries} | set(mapping.values())
    items = [build_review_item(pdf, bib_entries, mapping, existing_keys) for pdf in iter_queue_pdfs()]
    payload = {
        "workflow": "AI-assisted review",
        "paper_count": len(items),
        "papers": [asdict(item) for item in items],
    }
    save_review_queue(payload)
    write_mapping()

    for item in items:
        print(f"{item.filename}: {item.title} [{item.suggested_bib_key}]")
    print(f"Prepared review queue for {len(items)} paper(s).")
    return 0


def apply_decisions(decisions_path: Path) -> int:
    if not decisions_path.exists():
        print(f"Missing decisions file: {decisions_path}", file=sys.stderr)
        return 1

    decisions = json.loads(decisions_path.read_text(encoding="utf-8"))
    if not isinstance(decisions, dict):
        print("Decisions file must be a JSON object keyed by filename.", file=sys.stderr)
        return 1

    review_queue = load_review_queue()
    papers = {paper["filename"]: paper for paper in review_queue.get("papers", []) if isinstance(paper, dict) and "filename" in paper}
    processed = 0
    for pdf in iter_queue_pdfs():
        decision = decisions.get(pdf.name)
        if not isinstance(decision, dict):
            print(f"Missing decision for {pdf.name}", file=sys.stderr)
            return 1

        bucket = decision.get("decision")
        if bucket not in {"Relevant", "NotRelated"}:
            print(f"Invalid decision for {pdf.name}: {bucket}", file=sys.stderr)
            return 1

        bib_key = decision.get("bibtex_key")
        if not bib_key:
            queue_entry = papers.get(pdf.name, {})
            bib_key = queue_entry.get("suggested_bib_key") or mapping.get(pdf.name)
        if not bib_key:
            print(f"Missing bibtex key for {pdf.name}", file=sys.stderr)
            return 1

        target_dir = RELEVANT_DIR if bucket == "Relevant" else NOT_RELATED_DIR
        destination = resolve_destination(pdf, target_dir)
        if pdf.exists():
            shutil.move(str(pdf), str(destination))
        print(f"{pdf.name} -> {bucket} ({bib_key})")
        processed += 1

    write_mapping()
    print(f"Applied decisions for {processed} paper(s).")
    return 0


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    subparsers = parser.add_subparsers(dest="command")

    prepare_parser = subparsers.add_parser("prepare", help="Extract metadata, titles, and abstracts for AI review.")
    prepare_parser.set_defaults(command="prepare")

    apply_parser = subparsers.add_parser("apply", help="Apply reviewed decisions and move queued PDFs.")
    apply_parser.add_argument("decisions", help="Path to a JSON file keyed by PDF filename.")

    args = parser.parse_args()
    command = args.command or "prepare"

    if command == "prepare":
        return prepare_review_queue()
    if command == "apply":
        return apply_decisions(Path(args.decisions))

    parser.print_help()
    return 1


if __name__ == "__main__":
    raise SystemExit(main())
