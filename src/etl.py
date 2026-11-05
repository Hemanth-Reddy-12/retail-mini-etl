import sqlite3
from pathlib import Path

import pandas as pd


RAW_ORDERS_PATH = Path("data/raw/orders.csv")
PROCESSED_ORDERS_PATH = Path("data/processed/orders_clean.csv")
DATABASE_PATH = Path("db/orders.db")


def create_sample_orders(raw_path: Path) -> None:
    """Create a small sample CSV when no source orders file exists."""
    raw_path.parent.mkdir(parents=True, exist_ok=True)

    products = ["Coffee", "Tea", "Mug"]
    orders = []
    for order_number in range(1, 31):
        product = products[(order_number - 1) % len(products)]
        quantity = "" if order_number in (5, 14, 23) else (order_number % 4) + 1
        orders.append(
            {
                "order_id": order_number,
                "order_date": f"2025-01-{((order_number - 1) % 28) + 1:02d}",
                "product": product,
                "quantity": quantity,
                "unit_price": {"Coffee": 4.5, "Tea": 3.25, "Mug": 8.0}[product],
            }
        )

    pd.DataFrame(orders).to_csv(raw_path, index=False)


def run_etl(
    raw_path: Path = RAW_ORDERS_PATH,
    processed_path: Path = PROCESSED_ORDERS_PATH,
    database_path: Path = DATABASE_PATH,
) -> pd.DataFrame:
    """Create sample input if needed, clean orders, and save the results."""
    if not raw_path.exists():
        create_sample_orders(raw_path)

    orders = pd.read_csv(raw_path)
    orders["quantity"] = orders["quantity"].fillna(1).astype(int)
    orders["unit_price"] = pd.to_numeric(orders["unit_price"]).astype(float)
    orders["revenue"] = orders["quantity"] * orders["unit_price"]

    processed_path.parent.mkdir(parents=True, exist_ok=True)
    orders.to_csv(processed_path, index=False)

    database_path.parent.mkdir(parents=True, exist_ok=True)
    with sqlite3.connect(database_path) as connection:
        orders.to_sql("orders_clean", connection, if_exists="replace", index=False)

    total_orders = len(orders)
    total_revenue = orders["revenue"].sum()
    top_product = (
        orders.groupby("product")["revenue"].sum().idxmax()
        if not orders.empty
        else "N/A"
    )

    print(f"total_orders: {total_orders}")
    print(f"total_revenue: {total_revenue:.2f}")
    print(f"top_product_by_revenue: {top_product}")

    return orders


def main() -> None:
    run_etl()


if __name__ == "__main__":
    main()
