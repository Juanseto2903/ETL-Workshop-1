"""
main.py
Orchestrates the full ETL pipeline: Extract -> Transform -> Dimensional
Transformation. Loading to the Data Warehouse (Task 5) is handled
separately in load.py once the target database is configured.
"""

from extract import extract
from transform import transform
from dimensional_model import build_star_schema


def run_pipeline():
    print("=== ETL Pipeline: Recruitment Data Warehouse ===\n")

    raw_df = extract()
    prepared_df = transform(raw_df)
    tables = build_star_schema(prepared_df)

    print("\n=== Pipeline finished successfully ===")
    for name, table in tables.items():
        print(f"  {name}: {len(table):,} rows")

    return tables


if __name__ == "__main__":
    run_pipeline()