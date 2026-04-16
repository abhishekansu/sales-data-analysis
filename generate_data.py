import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import random
import os

random.seed(42)
np.random.seed(42)

# ── Config ────────────────────────────────────────────────────────────────────
PRODUCTS = {
    "Laptop Pro X1":    {"category": "Electronics",  "base_price": 1299},
    "Wireless Mouse":   {"category": "Accessories",  "base_price": 49},
    "USB-C Hub":        {"category": "Accessories",  "base_price": 79},
    "Monitor 27\"":     {"category": "Electronics",  "base_price": 449},
    "Mechanical KB":    {"category": "Accessories",  "base_price": 129},
    "Webcam HD":        {"category": "Electronics",  "base_price": 99},
    "Desk Lamp LED":    {"category": "Office",       "base_price": 59},
    "Standing Desk":    {"category": "Office",       "base_price": 599},
    "Chair Ergonomic":  {"category": "Office",       "base_price": 799},
    "Headphones Pro":   {"category": "Electronics",  "base_price": 299},
    "Tablet S10":       {"category": "Electronics",  "base_price": 649},
    "Phone Stand":      {"category": "Accessories",  "base_price": 29},
}

REGIONS = ["North", "South", "East", "West", "Central"]
CHANNELS = ["Online", "Retail", "B2B", "Reseller"]

SALES_REPS = [
    "Arjun Sharma", "Priya Patel", "Ravi Kumar",
    "Neha Singh", "Amit Verma", "Deepa Nair",
    "Karan Mehta", "Sunita Rao", "Vikram Das", "Pooja Iyer"
]

def generate_sales_data(n_rows=2000):
    start_date = datetime(2023, 1, 1)
    end_date   = datetime(2024, 12, 31)
    date_range = (end_date - start_date).days

    rows = []
    for i in range(n_rows):
        product_name = random.choice(list(PRODUCTS.keys()))
        product      = PRODUCTS[product_name]
        base_price   = product["base_price"]

        # Seasonal multiplier – Q4 peaks
        order_date   = start_date + timedelta(days=random.randint(0, date_range))
        month        = order_date.month
        seasonal     = 1.0 + 0.3 * np.sin((month - 3) * np.pi / 6)

        quantity     = random.choices([1, 2, 3, 4, 5], weights=[50, 25, 12, 8, 5])[0]
        discount_pct = random.choices([0, 5, 10, 15, 20], weights=[40, 25, 20, 10, 5])[0]
        unit_price   = round(base_price * seasonal * (1 + random.uniform(-0.05, 0.05)), 2)
        revenue      = round(unit_price * quantity * (1 - discount_pct / 100), 2)
        cost         = round(unit_price * quantity * random.uniform(0.45, 0.65), 2)
        profit       = round(revenue - cost, 2)

        rows.append({
            "order_id":    f"ORD-{10000 + i}",
            "order_date":  order_date.strftime("%Y-%m-%d"),
            "product":     product_name,
            "category":    product["category"],
            "region":      random.choice(REGIONS),
            "channel":     random.choice(CHANNELS),
            "sales_rep":   random.choice(SALES_REPS),
            "quantity":    quantity,
            "unit_price":  unit_price,
            "discount_pct": discount_pct,
            "revenue":     revenue,
            "cost":        cost,
            "profit":      profit,
        })

    df = pd.DataFrame(rows)
    df["order_date"] = pd.to_datetime(df["order_date"])
    return df


if __name__ == "__main__":
    os.makedirs("data", exist_ok=True)
    df = generate_sales_data(2000)
    df.to_csv("data/sales_data.csv", index=False)
    print(f"✅  Generated {len(df)} rows → data/sales_data.csv")
    print(df.head())
