#!/usr/bin/env python3
"""Generate bib_map.json from Relevant papers and reviewed decisions."""

from __future__ import annotations

import json
import sys
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parent.parent
REF_DIR = REPO_ROOT / "ref_papers"
RELEVANT_DIR = REF_DIR / "Relevant"
DECISIONS_FILE = REF_DIR / "review_decisions.json"
MAP_FILE = REF_DIR / "bib_map.json"


def build_mapping() -> dict[str, str]:
    if not DECISIONS_FILE.exists():
        print(f"Missing decisions file: {DECISIONS_FILE}", file=sys.stderr)
        raise SystemExit(1)

    decisions = json.loads(DECISIONS_FILE.read_text(encoding="utf-8"))
    if not isinstance(decisions, dict):
        print("review_decisions.json must be a JSON object keyed by filename.", file=sys.stderr)
        raise SystemExit(1)

    if not RELEVANT_DIR.exists():
        print(f"Missing Relevant directory: {RELEVANT_DIR}", file=sys.stderr)
        raise SystemExit(1)

    mapping: dict[str, str] = {}
    missing_decisions: list[str] = []
    missing_keys: list[str] = []

    for pdf_path in sorted(RELEVANT_DIR.glob("*.pdf"), key=lambda item: item.name.lower()):
        decision = decisions.get(pdf_path.name)
        if not isinstance(decision, dict) or decision.get("decision") != "Relevant":
            missing_decisions.append(pdf_path.name)
            continue

        bib_key = decision.get("bibtex_key")
        if not isinstance(bib_key, str) or not bib_key.strip():
            missing_keys.append(pdf_path.name)
            continue

        mapping[pdf_path.name] = bib_key.strip()

    if missing_decisions:
        print("Missing Relevant decisions for:", file=sys.stderr)
        for name in missing_decisions:
            print(f"  {name}", file=sys.stderr)
        raise SystemExit(1)

    if missing_keys:
        print("Missing bibtex_key for:", file=sys.stderr)
        for name in missing_keys:
            print(f"  {name}", file=sys.stderr)
        raise SystemExit(1)

    return mapping


def write_mapping() -> int:
    mapping = build_mapping()

    MAP_FILE.write_text(json.dumps(mapping, indent=2) + "\n", encoding="utf-8")
    print(f"Wrote {len(mapping)} Relevant paper mappings to {MAP_FILE.name}.")
    return 0


if __name__ == "__main__":
    raise SystemExit(write_mapping())
