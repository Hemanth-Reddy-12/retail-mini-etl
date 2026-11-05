# Retail Mini ETL

A beginner-friendly Python project for building a small ETL pipeline: extract data, transform it, and load the results.

## Run the project (PowerShell)

From the repository root:

1. Create and activate a virtual environment:

   ```powershell
   uv venv
   .\.venv\Scripts\Activate.ps1
   ```

2. Install the project dependencies:

   ```powershell
   uv pip install -r requirements.txt
   ```

3. Run the ETL starter script:

   ```powershell
   python src\etl.py
   ```

4. Run the tests:

   ```powershell
   python -m pytest
   ```
