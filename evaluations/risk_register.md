# Risk register

| Risk | Impact | Mitigation | Status |
|---|---|---|---|
| Incorrect business metrics from faulty joins/aggregation | Confidently wrong dashboard | Shared definitions; independent pandas check (`scripts/verify_totals.py`); tests against raw CSVs | In progress |
| Conversational answers that sound right but are wrong | Misleading answers | Approved questions only; show calculation; decline unsupported; benchmark with independently computed answers | Planned |
| Incorrect or misleading product imagery/links | Misrepresentation, rights issues | Original illustrations, labeled; no fabricated product URLs | Planned |
| Slide text states a number that doesn't match the data | Hallucinated insight | Slide numbers computed from data, not typed | Planned |
