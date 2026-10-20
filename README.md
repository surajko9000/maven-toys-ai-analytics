# Maven Toys AI Analytics Lab

An AI-generated analytics hub built on public data, hosted free on GitHub Pages. Built as a Chicago Booth
AI Essentials capstone and a portfolio project: how does AI change an analytics engineer's workflow, from
hand-assembling dashboards to describing data applications in plain language?

**Data:** [Maven Analytics – Mexico Toy Sales](https://mavenanalytics.io/data-playground/mexico-toy-sales)
(fictional retailer, public sample data). The app reads the four original CSVs directly in the browser. No database,
no server, no API keys.

## Four tabs, one dataset, one set of definitions

| Tab | Purpose |
|---|---|
| **Dashboard** | KPI cards, filters, trend and breakdown charts, sortable table, CSV export |
| **Presentation** | A paged mini-deck: one headline insight per slide, every number computed from the data |
| **Toy Finder** | Visual catalog of the 35 toys with detail view, comparison, stock by store |
| **Ask** | Chat-style Q&A that matches a typed question to ~20-30 verified questions; declines what it can't answer |

All tabs share `src/lib/metrics.ts`, so revenue, profit and margin mean the same thing everywhere.

## Status

Planning and data validation complete. Front-end build in progress. See `docs/architecture.md`.

## Honest limitations (so far)

- Revenue and profit are **reconstructed** (units x current price/cost); the data has no price history.
- Inventory is a single undated snapshot, not a history.
- "Latest week/quarter" means latest in the data (through 2023-09-30), not today.
- Ask answers only approved questions. It does not generate SQL or free-form answers.

## Repository layout

```
public/data/        original CSVs (unmodified)
data/               data dictionary and validation notes
scripts/            independent verification (pandas)
src/lib/            data loader + shared metric definitions
src/pages/          Dashboard, Presentation, ToyFinder, Ask
tests/              metric tests against the raw CSVs
evaluations/        prompt log, iteration log, benchmark, limitations, risks (capstone evidence)
docs/               architecture and capstone workflow notes
```

## Verify the headline numbers

```
python3 scripts/verify_totals.py
```

## Rebuild the deck

```
python3 scripts/build_deck.py            # writes site/deck/Colorbuds_to_Playfoam.pptx (asserts every number against the CSVs)
# then export the PDF and slide previews the site shows (needs LibreOffice + poppler):
soffice --headless --convert-to pdf --outdir site/deck site/deck/Colorbuds_to_Playfoam.pptx
pdftoppm -jpeg -r 110 site/deck/Colorbuds_to_Playfoam.pdf site/deck/preview/slide
```

## Rebuild the site and test the Ask matcher

```
python3 scripts/build_site.py <template.html> <data.json> <illustrations.json>   # splices data, art, Ask phrasing bank and test set into site/index.html
```

The Ask tab matches questions against `evaluations/ask_paraphrases.json` (about 200 example phrasings for the 15 approved questions).
`evaluations/ask_eval.json` holds held-out test phrasings. Open `site/index.html#ask-eval` in a browser (or dump the DOM headlessly) to see
the accuracy of the old keyword matcher versus the phrasing-bank matcher.
