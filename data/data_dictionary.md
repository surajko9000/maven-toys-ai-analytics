# Data dictionary

Source: [Maven Analytics – Mexico Toy Sales](https://mavenanalytics.io/data-playground/mexico-toy-sales),
a public sample dataset for a fictional retailer. The four CSVs in `public/data/` are the originals, unmodified.
All cleaning happens in code (`src/lib/data.ts`), never in the files.

## Files

| File | Rows | Grain | Key |
|---|---:|---|---|
| `sales.csv` | 829,262 | one transaction line | `Sale_ID` |
| `products.csv` | 35 | one product | `Product_ID` |
| `stores.csv` | 50 | one store | `Store_ID` |
| `inventory.csv` | 1,593 | one store x product (single undated snapshot) | (`Store_ID`, `Product_ID`) |

## Columns

**sales.csv**: `Sale_ID`, `Date` (2022-01-01 to 2023-09-30), `Store_ID`, `Product_ID`, `Units` (integer, 1 to 30).

**products.csv**: `Product_ID`, `Product_Name`, `Product_Category` (5 categories), `Product_Cost` and
`Product_Price` (text such as `$9.99 `, with `$` and a trailing space; parsed to numbers in code).

**stores.csv**: `Store_ID`, `Store_Name`, `Store_City` (29 cities), `Store_Location` (Downtown, Commercial,
Residential, Airport), `Store_Open_Date`. There are no coordinates.

**inventory.csv**: `Store_ID`, `Product_ID`, `Stock_On_Hand`.

## Validation results (profiled 2026-10-19)

- No nulls in any file. No orphan keys (every sale joins to one product and one store).
- `Sale_ID` is unique. About 741k rows share the same (date, store, product); they are separate
  transaction lines and **must not be de-duplicated**.
- Inventory: 1,593 of a possible 1,750 store-product pairs. 41 store-product pairs that sold have no inventory
  row (assumed "not stocked"; this is an assumption). 77 rows have zero stock.
- Every product's price is above its cost. Every product sold at least once.
- Data quirk: `Store_City` spells "Cuidad de Mexico" (4 stores). The app corrects the display name to
  "Ciudad de Mexico" and documents it here.

## Business definitions

| Metric | Definition | Caveat |
|---|---|---|
| Units sold | Sum of `Units` | |
| Revenue | Units x `Product_Price` | **Reconstructed**: one current price per product, no price history. Not accounting revenue. |
| Estimated gross profit | Units x (`Product_Price` - `Product_Cost`) | Same caveat; excludes all other costs. |
| Gross margin % | Estimated gross profit / Revenue | |
| Stock on hand | `Stock_On_Hand` from the snapshot | Current snapshot only; never summed across time. |
| Product popularity | Must be named explicitly: by units, by revenue, or by profit | "Best" alone is ambiguous. |
| "Latest" / "last quarter" | Relative to the last date in the data (2023-09-30), not today | |

## Reference totals (independent pandas calculation: `scripts/verify_totals.py`)

Rows 829,262 | Units 1,090,565 | Revenue $14,444,572.35 | Estimated gross profit $4,014,029.00 | Margin 27.79%
