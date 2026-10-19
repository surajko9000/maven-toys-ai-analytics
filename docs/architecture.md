# Architecture

```
Original CSVs (public/data/)  ->  browser fetch + parse (src/lib/data.ts)
                                   -> one row per date x store x product (units summed)
                                   -> metrics.ts (shared definitions)
                                        |-> Dashboard
                                        |-> Presentation
                                        |-> Toy Finder
                                        |-> Ask (approved questions + fuzzy matching)
GitHub Actions  ->  GitHub Pages (static)
```

## Decisions

| Decision | Why |
|---|---|
| Straight CSVs, no DuckDB/Parquet | Simplest to explain and reproduce; anyone can open the files and check the numbers. |
| Collapse 829k lines to one row per date x store x product at load | ~88k rows; revenue/profit are linear in units, so totals are exact and filters are instant. |
| One `metrics.ts` for all tabs | Single source of truth for definitions. |
| Ask = approved questions + fuzzy match (Fuse.js), embeddings only if the benchmark needs it | Every number is pre-verified; no model can invent a figure; works offline on static hosting. |
| 4 tabs, distinct by purpose | Dashboard (explore), Presentation (story), Toy Finder (app), Ask (conversation). |
| Hash routing | GitHub Pages has no server-side routing. |

## Constraints

Static hosting only, $0 recurring cost, no secrets in the repo, no account required for visitors.
