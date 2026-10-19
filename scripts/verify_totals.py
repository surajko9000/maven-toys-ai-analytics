"""Independent check of headline numbers, straight from the raw CSVs (pandas only).

Run: python3 scripts/verify_totals.py
These are the reference values the app's metrics.ts must reproduce.
"""
import sys
from pathlib import Path
import pandas as pd

DATA = Path(__file__).resolve().parent.parent / "public" / "data"
sales = pd.read_csv(DATA / "sales.csv", parse_dates=["Date"])
products = pd.read_csv(DATA / "products.csv")
for col in ("Product_Cost", "Product_Price"):
    products[col] = products[col].str.replace(r"[$ ]", "", regex=True).astype(float)

df = sales.merge(products, on="Product_ID", validate="many_to_one")
df["revenue"] = df.Units * df.Product_Price
df["profit"] = df.Units * (df.Product_Price - df.Product_Cost)

ref = {
    "rows": len(sales),
    "units": int(df.Units.sum()),
    "revenue": round(df.revenue.sum(), 2),
    "profit": round(df.profit.sum(), 2),
    "margin": round(df.profit.sum() / df.revenue.sum(), 4),
    "first_date": str(sales.Date.min().date()),
    "last_date": str(sales.Date.max().date()),
    "stores": int(sales.Store_ID.nunique()),
    "products": int(sales.Product_ID.nunique()),
}
for k, v in ref.items():
    print(f"{k:11} {v}")

expected = {"rows": 829262, "units": 1090565, "revenue": 14444572.35, "profit": 4014029.0,
            "first_date": "2022-01-01", "last_date": "2023-09-30"}
bad = {k: (ref[k], v) for k, v in expected.items() if ref[k] != v}
if bad:
    print("MISMATCH:", bad); sys.exit(1)
print("OK: matches the validated reference totals")
