import sqlite3

import pandas as pd

from src.etl import run_etl


def test_etl_cleans_and_saves_car_data(tmp_path):
    raw_path = tmp_path / "raw" / "cars.csv"
    raw_path.parent.mkdir(parents=True)
    pd.DataFrame(
        [
            {
                "Make": " Alpha ",
                "Model": "One",
                "Year": 2020,
                "Engine Fuel Type": None,
                "Engine HP": 100,
                "Engine Cylinders": 4,
                "Transmission Type": "AUTO",
                "Driven_Wheels": "front wheel drive",
                "Number of Doors": 4,
                "Market Category": None,
                "Vehicle Size": "Compact",
                "Vehicle Style": "Sedan",
                "highway MPG": 30,
                "city mpg": 20,
                "Popularity": 10,
                "MSRP": 20000,
            },
            {
                "Make": "Beta",
                "Model": "Two",
                "Year": 2021,
                "Engine Fuel Type": "regular unleaded",
                "Engine HP": 150,
                "Engine Cylinders": 4,
                "Transmission Type": "AUTO",
                "Driven_Wheels": "front wheel drive",
                "Number of Doors": 4,
                "Market Category": "Luxury",
                "Vehicle Size": "Midsize",
                "Vehicle Style": "Sedan",
                "highway MPG": 32,
                "city mpg": 22,
                "Popularity": 20,
                "MSRP": 30000,
            },
        ]
    ).to_csv(raw_path, index=False)

    processed_path = tmp_path / "processed" / "cars_clean.csv"
    database_path = tmp_path / "db" / "cars.db"
    cars, kpis = run_etl(raw_path, processed_path, database_path)

    assert len(cars) == 2
    assert cars.loc[0, "Make"] == "Alpha"
    assert cars.loc[0, "Engine Fuel Type"] == "Unknown"
    assert cars.loc[0, "Market Category"] == "Unknown"
    assert processed_path.exists()
    pd.testing.assert_frame_equal(pd.read_csv(processed_path), cars, check_dtype=False)
    assert database_path.exists()
    with sqlite3.connect(database_path) as connection:
        assert connection.execute("SELECT COUNT(*) FROM cars_clean").fetchone()[0] == 2
    assert kpis == {
        "vehicle_count": 2,
        "average_msrp": 25000.0,
        "top_make_by_average_msrp": "Beta",
    }


def test_etl_removes_duplicate_rows(tmp_path):
    raw_path = tmp_path / "raw" / "cars.csv"
    raw_path.parent.mkdir(parents=True)
    duplicate = {
        "Make": "Alpha",
        "Model": "One",
        "Year": 2020,
        "Engine Fuel Type": "regular unleaded",
        "Engine HP": 100,
        "Engine Cylinders": 4,
        "Transmission Type": "AUTO",
        "Driven_Wheels": "front wheel drive",
        "Number of Doors": 4,
        "Market Category": "Compact",
        "Vehicle Size": "Compact",
        "Vehicle Style": "Sedan",
        "highway MPG": 30,
        "city mpg": 20,
        "Popularity": 10,
        "MSRP": 20000,
    }
    pd.DataFrame([duplicate, duplicate]).to_csv(raw_path, index=False)

    cars, kpis = run_etl(
        raw_path,
        tmp_path / "processed" / "cars_clean.csv",
        tmp_path / "db" / "cars.db",
    )

    assert len(cars) == 1
    assert kpis["vehicle_count"] == 1
