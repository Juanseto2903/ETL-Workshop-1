"""
dimensional_model.py
Task 4 - Dimensional Transformation

Transforms the prepared/business-ruled candidate data into the star
schema defined in Task 2:
  Dim_Date, Dim_Technology, Dim_Candidate_Profile, Dim_Country, Fact_Application

Conceptually: Prepared Candidate Data -> Dimension Records -> Surrogate
Keys -> Key Mapping -> Fact Table.

Natural source values (dates, technology names, etc.) are never used as
primary keys. Every dimension gets its own sequential surrogate key
generated in this module.
"""

import pandas as pd

MONTH_NAMES = [
    "January", "February", "March", "April", "May", "June",
    "July", "August", "September", "October", "November", "December",
]


def build_dim_date(df: pd.DataFrame) -> pd.DataFrame:
    """One row per distinct Application Date, with a surrogate date_key."""
    dates = df["Application Date"].drop_duplicates().sort_values().reset_index(drop=True)

    dim_date = pd.DataFrame({"full_date": dates})
    dim_date.insert(0, "date_key", range(1, len(dim_date) + 1))
    dim_date["year"] = dim_date["full_date"].dt.year
    dim_date["quarter"] = dim_date["full_date"].dt.quarter
    dim_date["month"] = dim_date["full_date"].dt.month
    dim_date["month_name"] = dim_date["month"].apply(lambda m: MONTH_NAMES[m - 1])
    dim_date["day_of_week"] = dim_date["full_date"].dt.day_name()

    print(f"[build_dim_date] {len(dim_date):,} unique dates")
    return dim_date


def build_dim_technology(df: pd.DataFrame) -> pd.DataFrame:
    """One row per distinct Technology, with a surrogate technology_key."""
    technologies = df["Technology"].drop_duplicates().sort_values().reset_index(drop=True)

    dim_technology = pd.DataFrame({"technology_name": technologies})
    dim_technology.insert(0, "technology_key", range(1, len(dim_technology) + 1))

    print(f"[build_dim_technology] {len(dim_technology):,} unique technologies")
    return dim_technology


def build_dim_candidate_profile(df: pd.DataFrame) -> pd.DataFrame:
    """
    One row per distinct (Seniority, YOE_Range) combination, with a
    surrogate profile_key. Seniority and YOE_Range are modeled together
    because R3 requires analyzing hiring outcomes by both jointly.
    """
    profiles = (
        df[["Seniority", "YOE_Range"]]
        .drop_duplicates()
        .sort_values(["Seniority", "YOE_Range"])
        .reset_index(drop=True)
    )

    dim_profile = profiles.rename(
        columns={"Seniority": "seniority", "YOE_Range": "yoe_range"}
    )
    dim_profile.insert(0, "profile_key", range(1, len(dim_profile) + 1))

    print(f"[build_dim_candidate_profile] {len(dim_profile):,} unique seniority/YOE-range combinations")
    return dim_profile


def build_dim_country(df: pd.DataFrame) -> pd.DataFrame:
    """One row per distinct Country, with a surrogate country_key."""
    countries = df["Country"].drop_duplicates().sort_values().reset_index(drop=True)

    dim_country = pd.DataFrame({"country_name": countries})
    dim_country.insert(0, "country_key", range(1, len(dim_country) + 1))

    print(f"[build_dim_country] {len(dim_country):,} unique countries")
    return dim_country


def build_fact_application(
    df: pd.DataFrame,
    dim_date: pd.DataFrame,
    dim_technology: pd.DataFrame,
    dim_profile: pd.DataFrame,
    dim_country: pd.DataFrame,
) -> pd.DataFrame:
    """
    Maps each application to its dimension surrogate keys and builds the
    Fact_Application table at the declared grain: one row per candidate
    application.
    """
    fact = df.merge(dim_date, left_on="Application Date", right_on="full_date", how="left")
    fact = fact.merge(dim_technology, left_on="Technology", right_on="technology_name", how="left")
    fact = fact.merge(
        dim_profile, left_on=["Seniority", "YOE_Range"], right_on=["seniority", "yoe_range"], how="left"
    )
    fact = fact.merge(dim_country, left_on="Country", right_on="country_name", how="left")

    # Check for unmapped rows (would indicate a key-mapping problem)
    key_cols = ["date_key", "technology_key", "profile_key", "country_key"]
    unmapped = fact[key_cols].isnull().any(axis=1).sum()
    if unmapped:
        raise ValueError(f"[build_fact_application] {unmapped} rows failed to map to a dimension key")

    fact_application = fact[
        [
            "date_key",
            "technology_key",
            "profile_key",
            "country_key",
            "Code Challenge Score",
            "Technical Interview Score",
            "Hired",
        ]
    ].rename(
        columns={
            "Code Challenge Score": "code_challenge_score",
            "Technical Interview Score": "technical_interview_score",
            "Hired": "hired_flag",
        }
    )
    fact_application["application_count"] = 1
    fact_application.insert(0, "application_key", range(1, len(fact_application) + 1))

    print(f"[build_fact_application] {len(fact_application):,} fact rows, 0 unmapped keys")
    return fact_application


def build_star_schema(df: pd.DataFrame) -> dict:
    """Runs the full dimensional transformation and returns all five tables."""
    dim_date = build_dim_date(df)
    dim_technology = build_dim_technology(df)
    dim_profile = build_dim_candidate_profile(df)
    dim_country = build_dim_country(df)
    fact_application = build_fact_application(df, dim_date, dim_technology, dim_profile, dim_country)

    return {
        "dim_date": dim_date,
        "dim_technology": dim_technology,
        "dim_candidate_profile": dim_profile,
        "dim_country": dim_country,
        "fact_application": fact_application,
    }


if __name__ == "__main__":
    from extract import extract
    from transform import transform

    raw_df = extract()
    prepared_df = transform(raw_df)
    tables = build_star_schema(prepared_df)

    for name, table in tables.items():
        print(f"\n{name} ({len(table):,} rows):")
        print(table.head())