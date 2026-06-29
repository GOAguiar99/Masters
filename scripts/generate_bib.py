#!/usr/bin/env python3
"""Generate BibTeX entries from PDF metadata."""

import json
import re
import subprocess
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
REF_DIR = REPO_ROOT / "ref_papers"
MAP_FILE = REF_DIR / "bib_map.json"
BIB_FILE = REPO_ROOT / "aftertext" / "references.bib"

def run_command(*args: str) -> str:
    completed = subprocess.run(args, check=False, capture_output=True, text=True)
    if completed.returncode != 0:
        return ""
    return completed.stdout

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
        if lowered.startswith(("accepted for publication", "article in press", "contents lists available", "journal homepage", "see discussions, stats", "invited paper", "special section on")):
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
    if meta_title and meta_title.lower() not in ("ieee paper template in a4 (v1)", "untitled"):
        return " ".join(meta_title.split()), 0

    lines = clean_lines(text)
    title_lines: list[str] = []
    consumed = 0
    for line in lines[:20]:
        lowered = line.lower()
        if lowered.startswith(("abstract", "keywords:", "index terms", "doi", "issn", "volume", "number", "pages", "journal", "conference", "proceedings", "ieee", "acm", "springer", "elsevier", "wiley")) and title_lines:
            break
        if looks_like_author_line(line) and title_lines:
            break
        if lowered.startswith(("wireless netw", "computer communications", "journal of ", "ieice trans.", "international journal", "mobile computing", "electronics", "applied sciences", "computers", "sensors", "arXiv", "arxiv")):
            continue
        if re.match(r"\d{4}", line):  # Skip lines starting with year
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
    if meta_author and not meta_author.lower().startswith("unknown"):
        return meta_author
    scan = lines[title_line_count:title_line_count + 10] if title_line_count else lines[:15]
    for line in scan:
        if looks_like_author_line(line):
            # Clean the line: remove emails, affiliations
            cleaned = re.sub(r'\s*\([^)]*\)\s*', '', line)  # Remove parentheses
            cleaned = re.sub(r'\s*@\s*\S+', '', cleaned)  # Remove emails
            cleaned = re.sub(r'\s*,?\s*(university|department|school|institute|faculty|lab|center)\s+.*', '', cleaned, flags=re.IGNORECASE)
            return cleaned.strip()
    return "Unknown Author"

def extract_year(info: dict[str, str], text: str) -> str:
    candidates = re.findall(r"\b(19\d{2}|20[0-3]\d)\b", text)
    if candidates:
        preferred = [candidate for candidate in candidates if 2000 <= int(candidate) <= 2030] or candidates
        from collections import Counter
        counts = Counter(preferred)
        return sorted(counts.items(), key=lambda item: (-item[1], int(item[0])))[0][0]
    creation = info.get("CreationDate", "")
    match = re.search(r"(19\d{2}|20[0-3]\d)", creation)
    if match:
        return match.group(1)
    return "0000"

def generate_bibtex(key: str, title: str, author_hint: str, year: str) -> str:
    # Simple BibTeX generation, assuming @article
    authors = author_hint.replace(" and ", " and ")
    bib = f"@article{{{key},\n"
    bib += f"  title={{{title}}},\n"
    bib += f"  author={{{authors}}},\n"
    bib += f"  year={{{year}}},\n"
    bib += "}\n"
    return bib

def main():
    mapping = json.loads(MAP_FILE.read_text(encoding="utf-8"))
    existing_bib = BIB_FILE.read_text(encoding="utf-8")
    existing_keys = set(re.findall(r"@[a-zA-Z]+{([^,]+),", existing_bib))
    new_entries: list[str] = []
    added = 0

    for pdf_name, bib_key in mapping.items():
        if bib_key in existing_keys:
            continue
        pdf_path = REF_DIR / "Relevant" / pdf_name
        if not pdf_path.exists():
            print(f"PDF not found: {pdf_name}", file=sys.stderr)
            continue

        info = extract_pdf_info(pdf_path)
        text = extract_text(pdf_path, pages=2)
        lines = clean_lines(text)
        title, title_line_count = extract_title(info, text, pdf_path)
        author_hint = extract_author_hint(info, lines, title_line_count, pdf_path)
        year = extract_year(info, text)

        bib_entry = generate_bibtex(bib_key, title, author_hint, year)
        new_entries.append(bib_entry)
        existing_keys.add(bib_key)
        added += 1
        print(f"Queued {bib_key} for append to {BIB_FILE.name}")

    if not new_entries:
        print("No new BibTeX entries to add.")
        return

    with open(BIB_FILE, "a", encoding="utf-8") as handle:
        if existing_bib and not existing_bib.endswith("\n"):
            handle.write("\n")
        handle.write("\n")
        handle.write("\n".join(entry.rstrip() for entry in new_entries))
        handle.write("\n")

    print(f"Appended {added} new entr{'y' if added == 1 else 'ies'} to {BIB_FILE.name}.")

if __name__ == "__main__":
    main()
