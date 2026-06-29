# Reference Paper Workflow

Local reference PDFs are handled as an AI-assisted queue rather than a pure keyword classifier.

## Structure

- `ref_papers/Analysis/`: manual input queue for new PDFs
- `ref_papers/Relevant/`: papers that directly or indirectly support the thesis
- `ref_papers/NotRelated/`: papers that do not help the thesis
- `ref_papers/bib_map.json`: filename-to-BibTeX-key mapping for `Relevant/` papers only
- `ref_papers/review_queue.json`: extracted metadata and abstracts for AI review

## Review rule

A paper is marked `Relevant` when it aligns with the thesis context around QoS, Wi-Fi / IEEE 802.11, V2X, vehicular networking, scheduling, OMNeT++, Veins, INET, or closely related networking and real-time systems topics.

If a paper is borderline but still useful, treat it as `Relevant`.

## Processing

Step 1: prepare the review queue.

```bash
cd /home/aguiar/master/Masters
python3 scripts/process_ref_papers.py prepare
```

Step 2: ask AI to review the queue and produce decisions using the extracted summaries.

Expected decision format in `ref_papers/review_decisions.json`:

```json
{
  "paper_filename.pdf": {
    "decision": "Relevant",
    "bibtex_key": "AuthorYearKeyword"
  }
}
```

Step 3: apply the reviewed decisions.

```bash
python3 scripts/process_ref_papers.py apply ref_papers/review_decisions.json
```

Step 4: generate `bib_map.json` from the `Relevant/` folder only.

```bash
python3 scripts/generate_bib_map.py
```

Step 5: append missing BibTeX entries to the dissertation bibliography.

```bash
python3 scripts/generate_bib.py
```

This reads `ref_papers/bib_map.json` and adds only missing entries to `aftertext/references.bib`.

The `ref_papers/` directory is for private local context only and must not be committed.
