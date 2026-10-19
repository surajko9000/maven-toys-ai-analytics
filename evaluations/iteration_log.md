# Iteration log (capstone evidence)

Record what actually happens. Do not pre-write findings.

| # | Date | Phase | Prompt / change | Result | Errors found | Fix | AI time | Manual verify time | Manual code edits |
|---|---|---|---|---|---|---|---|---|---|
| 1 | 2026-10-19 | Planning | Project brief given to Claude Code; asked to plan before building | Revised scope: 5 tabs -> 4 tabs, DuckDB dropped, Ask simplified to approved questions | Initial guess that data covered 2017-2018 was wrong (actual 2022-01-01 to 2023-09-30) | Profiled the real files | | | 0 |
| 2 | 2026-10-19 | Data validation | Uploaded 4 CSVs; asked Claude to profile them | Found: price/cost stored as text, shared date/store/product keys, partial inventory, city typo, no coordinates | | Documented in `data/data_dictionary.md` | | | 0 |
| 3 | 2026-10-19 | Environment | Asked Claude to create GitHub repo | Blocked: sandbox cannot create repos; user created it. Push needed GitHub App install. npm registry blocked by network policy. | Environment limits, not code | User adjusted settings | | | |
| 4 | 2026-10-19 | Mockup v1 | Asked Claude for a clickable 4-tab mockup on the real CSV data | Worked; numbers spot-checked vs pandas | None found in v1 | n/a | | | 0 |
| 5 | 2026-10-19 | Mockup v2 | Feedback: playful theme, Start-here tab, time filter, toy dropdown, clearer sort, better Ask | Implemented. Testing found Ask bugs: a month regex matched inside words ("margn" read as March) via an operator-precedence slip; store labels truncated; an awkward follow-up chip | 3 bugs in AI-written code, caught by trying typo/odd queries | Fixed, re-tested vs pandas | | | 0 |

## Timers to keep (the user fills these in)
- Time to first functional prototype:
- Total development time:
- Manual code changes (git author vs. Claude-authored commits):
