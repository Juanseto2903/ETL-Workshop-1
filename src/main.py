"""
main.py
Orchestrates the full ETL pipeline: Extract -> Transform -> Dimensional
Transformation -> Load (MySQL).

Run with `python src/main.py` from the repository root. Requires a
.env file with local MySQL credentials (see .env.example).
"""

from extract import extract
from transform import transform
from dimensional_model import build_star_schema
from load import create_schema, load_star_schema


def run_pipeline(load_to_db: bool = True):
    print("=== ETL Pipeline: Recruitment Data Warehouse ===\n")

    raw_df = extract()
    prepared_df = transform(raw_df)
    tables = build_star_schema(prepared_df)

    print("\n=== Dimensional transformation finished ===")
    for name, table in tables.items():
        print(f"  {name}: {len(table):,} rows")

    if load_to_db:
        print("\n=== Loading Data Warehouse (MySQL) ===")
        create_schema()
        load_star_schema(tables)

    return tables

if __name__ == "__main__":
    run_pipeline()