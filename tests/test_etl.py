import pandas as pd

from src.etl import run_etl


def test_revenue_column_exists_and_non_negative(tmp_path):
    raw_path = tmp_path / "raw" / "orders.csv"
    processed_path = tmp_path / "processed" / "orders_clean.csv"
    database_path = tmp_path / "db" / "orders.db"

    orders = run_etl(raw_path, processed_path, database_path)

    assert "revenue" in orders.columns
    assert (orders["revenue"] >= 0).all()
    assert processed_path.exists()
    assert database_path.exists()


def test_missing_quantity_filled_with_one(tmp_path):
    raw_path = tmp_path / "raw" / "orders.csv"
    raw_path.parent.mkdir(parents=True)
    pd.DataFrame(
        [
            {
                "order_id": 1,
                "order_date": "2025-01-01",
                "product": "Coffee",
                "quantity": None,
                "unit_price": 4.5,
            }
        ]
    ).to_csv(raw_path, index=False)

    orders = run_etl(
        raw_path,
        tmp_path / "processed" / "orders_clean.csv",
        tmp_path / "db" / "orders.db",
    )

    assert orders.loc[0, "quantity"] == 1
    assert orders.loc[0, "revenue"] == 4.5
