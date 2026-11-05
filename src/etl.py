import sqlite3
from pathlib import Path

import pandas as pd


PROJECT_ROOT = Path(__file__).resolve().parents[1]
RAW_DATA_PATH = PROJECT_ROOT / "data" / "raw" / "car_features_msrp.csv"
PROCESSED_DATA_PATH = PROJECT_ROOT / "data" / "processed" / "cars_clean.csv"
DATABASE_PATH = PROJECT_ROOT / "db" / "cars.db"

CATEGORICAL_COLUMNS = ["Engine Fuel Type", "Market Category"]
NUMERIC_COLUMNS = [
    "Year",
    "Engine HP",
    "Engine Cylinders",
    "Number of Doors",
    "highway MPG",
    "city mpg",
    "Popularity",
    "MSRP",
]


def run_etl(
    raw_path: Path = RAW_DATA_PATH,
    processed_path: Path = PROCESSED_DATA_PATH,
    database_path: Path = DATABASE_PATH,
) -> tuple[pd.DataFrame, dict[str, int | float | str]]:
    """Clean car data, save CSV and SQLite outputs, and report summary KPIs."""
    raw_path = Path(raw_path)
    processed_path = Path(processed_path)
    database_path = Path(database_path)

    if not raw_path.exists():
        raise FileNotFoundError(f"Car dataset not found: {raw_path}")

    cars = pd.read_csv(raw_path)
    required_columns = {"Make", "MSRP", *CATEGORICAL_COLUMNS, *NUMERIC_COLUMNS}
    missing_columns = required_columns.difference(cars.columns)
    if missing_columns:
        missing_list = ", ".join(sorted(missing_columns))
        raise ValueError(f"Car dataset is missing required columns: {missing_list}")

    for column in cars.select_dtypes(include=["object", "string"]).columns:
        cars[column] = cars[column].astype("string").str.strip()
        cars[column] = cars[column].replace("", pd.NA)

    for column in CATEGORICAL_COLUMNS:
        cars[column] = cars[column].fillna("Unknown")

    for column in NUMERIC_COLUMNS:
        cars[column] = pd.to_numeric(cars[column], errors="raise")

    cars = cars.drop_duplicates().reset_index(drop=True)
    if cars.empty:
        raise ValueError("Car dataset has no rows to process.")

    processed_path.parent.mkdir(parents=True, exist_ok=True)
    cars.to_csv(processed_path, index=False)

    database_path.parent.mkdir(parents=True, exist_ok=True)
    with sqlite3.connect(database_path) as connection:
        cars.to_sql("cars_clean", connection, if_exists="replace", index=False)

    kpis: dict[str, int | float | str] = {
        "vehicle_count": len(cars),
        "average_msrp": float(cars["MSRP"].mean()),
        "top_make_by_average_msrp": str(
            cars.groupby("Make")["MSRP"].mean().idxmax()
        ),
    }

    print(f"vehicle_count: {kpis['vehicle_count']}")
    print(f"average_msrp: ${kpis['average_msrp']:,.2f}")
    print(f"top_make_by_average_msrp: {kpis['top_make_by_average_msrp']}")
    return cars, kpis


def main() -> None:
    run_etl()


if __name__ == "__main__":
    main()
