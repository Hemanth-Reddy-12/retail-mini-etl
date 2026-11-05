# Retail Mini ETL

A beginner-friendly ETL project using Kaggle's [Car Features and MSRP dataset](https://www.kaggle.com/datasets/CooperUnion/cardataset).
The CSV source is in `data/raw/car_features_msrp.csv`.

The pipeline trims text, fills missing fuel type and market category with
`Unknown`, converts numeric fields, and removes exact duplicate rows. Numeric
values that are missing in the source are kept missing. It writes cleaned
records to `data/processed/cars_clean.csv` and replaces the `cars_clean` table
in `db/cars.db`.

It also prints the vehicle count, average MSRP, and make with the highest
average MSRP.

## Run the project (PowerShell)

From the repository root:

1. Create and activate a virtual environment:

   ```powershell
   uv venv
   .\.venv\Scripts\Activate.ps1
   ```

2. Install dependencies:

   ```powershell
   uv pip install -r requirements.txt
   ```

3. Run the ETL:

   ```powershell
   python src\etl.py
   ```

4. Run tests:

   ```powershell
   python -m pytest
   ```
