"""
load.py
Task 5 - Load the Data Warehouse (MySQL)

Connects to a local MySQL instance using credentials from a .env file
(never hardcoded), executes create_tables.sql to (re)build the schema,
and loads the dimension and fact tables in the correct order:
    Dimensions -> Fact Table

After loading, validates row counts, referential integrity, and the
absence of invalid dimension references.
"""

import os
from pathlib import Path

import pandas as pd
from dotenv import load_dotenv
from sqlalchemy import create_engine, text

load_dotenv()

DB_USER = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("DB_PASSWORD")
DB_HOST = os.getenv("DB_HOST", "localhost")
DB_PORT = os.getenv("DB_PORT", "3306")
DB_NAME = os.getenv("DB_NAME", "recruitment_dw")

CREATE_TABLES_SQL_PATH = Path("sql/create_tables.sql")


def get_engine(with_database: bool = True):
    """
    Builds a SQLAlchemy engine for the local MySQL instance.
    with_database=False connects without selecting a database, needed
    the first time create_tables.sql runs `CREATE DATABASE IF NOT EXISTS`.
    """
    db_part = f"/{DB_NAME}" if with_database else "/"
    url = f"mysql+pymysql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}{db_part}"
    return create_engine(url)


def create_schema():
    """Executes create_tables.sql against the local MySQL server."""
    sql_script = CREATE_TABLES_SQL_PATH.read_text()
    statements = [s.strip() for s in sql_script.split(";") if s.strip()]

    engine = get_engine(with_database=False)
    with engine.begin() as conn:
        for statement in statements:
            conn.execute(text(statement))

    print(f"[create_schema] Executed {len(statements)} statements from {CREATE_TABLES_SQL_PATH}")


def load_table(engine, df: pd.DataFrame, table_name: str):
    """Appends a DataFrame into an existing MySQL table."""
    df.to_sql(table_name, con=engine, if_exists="append", index=False, chunksize=5000)
    print(f"[load_table] Loaded {len(df):,} rows into '{table_name}'")


def load_star_schema(tables: dict):
    """
    Loads the star schema into MySQL in the correct order:
    dimensions first, then the fact table.
    """
    engine = get_engine()

    load_table(engine, tables["dim_date"], "dim_date")
    load_table(engine, tables["dim_technology"], "dim_technology")
    load_table(engine, tables["dim_candidate_profile"], "dim_candidate_profile")
    load_table(engine, tables["dim_country"], "dim_country")
    load_table(engine, tables["fact_application"], "fact_application")

    validate_load(engine, tables)


def validate_load(engine, tables: dict):
    """
    Validates that the load was successful:
      - Row counts in the DW match the DataFrame row counts.
      - No fact rows reference a non-existent dimension key
        (relies on FOREIGN KEY constraints, double-checked here with NULL joins).
    """
    print("\n[validate_load] Row count checks:")
    with engine.connect() as conn:
        for name, table_name in [
            ("dim_date", "dim_date"),
            ("dim_technology", "dim_technology"),
            ("dim_candidate_profile", "dim_candidate_profile"),
            ("dim_country", "dim_country"),
            ("fact_application", "fact_application"),
        ]:
            db_count = conn.execute(text(f"SELECT COUNT(*) FROM {table_name}")).scalar()
            expected = len(tables[name])
            status = "OK" if db_count == expected else "MISMATCH"
            print(f"  {table_name}: expected={expected:,} loaded={db_count:,} [{status}]")

        invalid_refs = conn.execute(
            text(
                """
                SELECT COUNT(*) FROM fact_application f
                LEFT JOIN dim_date d ON f.date_key = d.date_key
                LEFT JOIN dim_technology t ON f.technology_key = t.technology_key
                LEFT JOIN dim_candidate_profile p ON f.profile_key = p.profile_key
                LEFT JOIN dim_country c ON f.country_key = c.country_key
                WHERE d.date_key IS NULL
                   OR t.technology_key IS NULL
                   OR p.profile_key IS NULL
                   OR c.country_key IS NULL
                """
            )
        ).scalar()
        print(f"\n[validate_load] Fact rows with invalid dimension references: {invalid_refs}")


if __name__ == "__main__":
    from extract import extract
    from transform import transform
    from dimensional_model import build_star_schema

    raw_df = extract()
    prepared_df = transform(raw_df)
    star_schema_tables = build_star_schema(prepared_df)

    create_schema()
    load_star_schema(star_schema_tables)