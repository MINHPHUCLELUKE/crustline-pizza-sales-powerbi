"""Recompute the headline figures of the Crustline report straight from the raw CSV.

This is check 23 in docs/qa_checklist.md. It uses no Power Query steps and no Power BI
model, so it is an independent test of the report.

Usage:
    pip install pandas
    python qa/check_totals.py path/to/data_pizza.csv

The script prints one line per check and exits with code 1 if any check fails.
The CSV is not included in this repository.
"""
import sys

import pandas as pd

# Expected values: the figures shown in the report and in the README.
EXPECTED = {
    "rows": 48620,
    "orders": 21350,
    "pizzas sold": 49574,
    "revenue": 817860.05,
    "pizza ids (pizza and size)": 91,
    "trading days": 358,
    "daily average revenue": 2284.53,
    "daily revenue std dev (population)": 405.38,
    "anomaly days (|z| >= 2)": 16,
    "spike days (z >= 2)": 11,
    "drop days (z <= -2)": 5,
    "average order value": 38.31,
    "average pizzas per order": 2.32,
    "single item orders": 8201,
    "multi item orders": 13149,
    "orders with 1 pizza": 8111,
    "orders with 2 pizzas": 6152,
    "orders with 3 pizzas": 3207,
    "orders with 4 or more pizzas": 3880,
    "units Classic": 14888,
    "units Supreme": 11987,
    "units Veggie": 11649,
    "units Chicken": 11050,
    "revenue Classic": 220053.10,
    "revenue Supreme": 208197.00,
    "revenue Veggie": 193690.45,
    "revenue Chicken": 195919.50,
    "units S": 14403,
    "units M": 15635,
    "units L": 18956,
    "units XL": 552,
    "units XXL": 28,
    "days without orders": 7,
}


def compute(path):
    # The source file is not UTF-8 (one stray byte before "Nduja"), so read it as latin-1.
    d = pd.read_csv(path, encoding="latin-1")
    d["revenue"] = d["quantity"] * d["price"]
    d["date"] = pd.to_datetime(d["date"])

    daily = d.groupby("date")["revenue"].sum()
    mean, sd = daily.mean(), daily.std(ddof=0)
    z = (daily - mean) / sd
    all_days = pd.date_range("2015-01-01", "2015-12-31")

    distinct_per_order = d.groupby("order_id")["pizza_id"].nunique()
    pizzas_per_order = d.groupby("order_id")["quantity"].sum().clip(upper=4)
    by_cat = d.groupby("category").agg(q=("quantity", "sum"), r=("revenue", "sum"))
    by_size = d.groupby("size")["quantity"].sum()

    orders = d["order_id"].nunique()
    got = {
        "rows": len(d),
        "orders": orders,
        "pizzas sold": int(d["quantity"].sum()),
        "revenue": d["revenue"].sum(),
        "pizza ids (pizza and size)": d["pizza_id"].nunique(),
        "trading days": len(daily),
        "daily average revenue": mean,
        "daily revenue std dev (population)": sd,
        "anomaly days (|z| >= 2)": int((z.abs() >= 2).sum()),
        "spike days (z >= 2)": int((z >= 2).sum()),
        "drop days (z <= -2)": int((z <= -2).sum()),
        "average order value": d["revenue"].sum() / orders,
        "average pizzas per order": d["quantity"].sum() / orders,
        "single item orders": int((distinct_per_order == 1).sum()),
        "multi item orders": int((distinct_per_order > 1).sum()),
        "orders with 1 pizza": int((pizzas_per_order == 1).sum()),
        "orders with 2 pizzas": int((pizzas_per_order == 2).sum()),
        "orders with 3 pizzas": int((pizzas_per_order == 3).sum()),
        "orders with 4 or more pizzas": int((pizzas_per_order == 4).sum()),
        "days without orders": len(set(all_days) - set(daily.index)),
    }
    for cat in ["Classic", "Supreme", "Veggie", "Chicken"]:
        got[f"units {cat}"] = int(by_cat.loc[cat, "q"])
        got[f"revenue {cat}"] = by_cat.loc[cat, "r"]
    for size in ["S", "M", "L", "XL", "XXL"]:
        got[f"units {size}"] = int(by_size.loc[size])
    return got


def main():
    if len(sys.argv) != 2:
        sys.exit(__doc__)
    got = compute(sys.argv[1])
    failures = 0
    for name, expected in EXPECTED.items():
        value = got[name]
        ok = abs(value - expected) < 0.005 if isinstance(expected, float) else value == expected
        failures += not ok
        fmt = ",.2f" if isinstance(expected, float) else ","
        print(f"{'PASS' if ok else 'FAIL'}  {name:<38} expected {expected:>12{fmt}}  got {value:>12{fmt}}")
    print(f"\n{len(EXPECTED) - failures} of {len(EXPECTED)} checks passed")
    sys.exit(1 if failures else 0)


if __name__ == "__main__":
    main()
