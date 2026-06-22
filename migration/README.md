# migration/ — provenance (one-time)

This folder documents **how the enriched catalog was first built**. It is not part
of the ongoing workflow and is safe to ignore for day-to-day edits.

The live flow is: edit [`../data/*.csv`](../data/) → run
[`../build_site.py`](../build_site.py) → `index.json` + `AUDIT.md`.
The data now lives in **CSV**; the original Excel workbook
(`iotc-index-catalog.xlsx`) is archived here as the pre-CSV snapshot.

## What's here

| File | What it is |
|---|---|
| `_wb_dump.json` | Snapshot of the **original** workbook (Listings/Boards/Config) before enrichment. |
| `_overlay.json` | Harvested overlay: 188 per-board resources, 27 new listings, topic assignments, board-ref fixes, new boards — extracted from `avnet-iotconnect.github.io` and reconciled. |
| `_partner_img_map.json` | Part-Number → local image + Avnet buy-link map, parsed from the partner READMEs. |
| `_review.json` | Adversarial review findings (front-end a11y, data accuracy, completeness) that were folded into the build. |
| `build_catalog.py` | The generator that fused the three inputs into the enriched workbook + Resources sheet. |
| `fill_listings.py` | One-time fill of missing Listings cells (languages/links/repos/topics) + the `Image` column. |
| `xlsx_to_csv.py` | One-time conversion of the workbook into `../data/*.csv` (the current source of truth). |
| `iotc-index-catalog.xlsx` | Archived pre-CSV Excel workbook (superseded by `../data/*.csv`). |
| `_research.json` / `_listings.json` | Web-research patches + listing snapshot used by `fill_listings.py`. |
| `_linkcheck.py` | Liveness checker for every URL in `../index.json` (run: `python migration/_linkcheck.py`). |

## ⚠ Do not re-run `build_catalog.py` casually

It regenerates `../iotc-index-catalog.xlsx` from `_wb_dump.json` (the *pre-migration*
snapshot) plus the overlay. Re-running it **discards any hand-edits** made to the
workbook since the migration. The workbook is now the source of truth — edit it
directly. `build_catalog.py` is kept only for provenance / reproducibility.
