# Iteration log (capstone evidence)

Record what actually happens. Do not pre-write findings.

| # | Date | Phase | Prompt / change | Result | Errors found | Fix | AI time | Manual verify time | Manual code edits |
|---|---|---|---|---|---|---|---|---|---|
| 1 | 2026-10-19 | Planning | Project brief given to Claude Code; asked to plan before building | Revised scope: 5 tabs -> 4 tabs, DuckDB dropped, Ask simplified to approved questions | Initial guess that data covered 2017-2018 was wrong (actual 2022-01-01 to 2023-09-30) | Profiled the real files | | | 0 |
| 2 | 2026-10-19 | Data validation | Uploaded 4 CSVs; asked Claude to profile them | Found: price/cost stored as text, shared date/store/product keys, partial inventory, city typo, no coordinates | | Documented in `data/data_dictionary.md` | | | 0 |
| 3 | 2026-10-19 | Environment | Asked Claude to create GitHub repo | Blocked: sandbox cannot create repos; user created it. Push needed GitHub App install. npm registry blocked by network policy. | Environment limits, not code | User adjusted settings | | | |

## Timers to keep (the user fills these in)
- Time to first functional prototype:
- Total development time:
- Manual code changes (git author vs. Claude-authored commits):
