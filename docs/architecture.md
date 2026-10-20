# Architecture

```
public/data/*.csv  --scripts/gen_data.py-->  compact data  \
scripts/mockup_illustrations_all.py -------->  toy drawings  }--scripts/build_site.py-->  site/index.html  --GitHub Actions-->  GitHub Pages
evaluations/ask_*.json --------------------->  Ask phrasings /          (template: site-src/template.html)

In the browser: one agg() function computes revenue / profit / units from the compact data for every tab
  -> Dashboard, Toy Finder, Presentation viewer, Ask
Deck: scripts/build_deck.py (python-pptx) -> site/deck/*.pptx / .pdf / preview images
```

## Decisions

| Decision | Why |
|---|---|
| Straight CSVs, no DuckDB/Parquet | Simplest to explain and reproduce; anyone can open the files and check the numbers. |
| Collapse 829k lines to one row per date x store x product at load | ~88k rows; revenue/profit are linear in units, so totals are exact and filters are instant. |
| One shared `agg()` function for all tabs | Single source of truth for definitions, so a number means the same thing everywhere. |
| Ask = approved questions matched by a phrasing bank (keywords), plus an optional in-browser embedding model | Every number is pre-verified; no model can invent a figure; works offline on static hosting. |
| 5 tabs, distinct by purpose | Home (overview), Dashboard (explore), Toy Finder (app), Presentation (story), Ask (conversation). |
| Hash routing | GitHub Pages has no server-side routing. |

## Constraints

Static hosting only, $0 recurring cost, no secrets in the repo, no account required for visitors.
