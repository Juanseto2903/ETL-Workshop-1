"""
transform.py
Task 3.2 - Data Preparation
Task 3.3 - Business Transformation

Applies only the preparation required by the analytical model, then
implements the hiring business rule and the derived attributes needed
by the five business requirements (R1-R5).

All preparation decisions are documented inline as comments.
"""

import pandas as pd


def prepare(df: pd.DataFrame) -> pd.DataFrame:
    """
    Task 3.2 - Data Preparation.

    Decisions made (see Task 1 profiling for the evidence behind each one):
      - Application Date is converted from string to datetime. Profiling
        showed 0 unparseable values, so no rows are lost in this step.
      - Text columns used later as dimension attributes (Country, Seniority,
        Technology) are stripped of leading/trailing whitespace to guard
        against accidental formatting issues, even though profiling found
        no inconsistent casing or typos.
      - No rows are dropped for missing values, because profiling found 0
        missing values in the entire dataset.
      - The 167 duplicate email addresses found during profiling are NOT
        removed. The declared grain of the fact table is "one application",
        not "one unique candidate identity", and profiling confirmed there
        are no duplicates on (First Name, Last Name, Email) together - so
        each row still represents a distinct, valid application event.
        This decision is documented rather than silently dropping rows.
    """
    df = df.copy()

    df["Application Date"] = pd.to_datetime(df["Application Date"], errors="raise")

    for col in ["Country", "Seniority", "Technology"]:
        df[col] = df[col].str.strip()

    print(f"[prepare] {len(df):,} rows after data preparation (no rows dropped)")
    return df


def apply_business_rules(df: pd.DataFrame) -> pd.DataFrame:
    """
    Task 3.3 - Business Transformation.

    - Hired flag: HIRED = (Code Challenge Score >= 7) AND (Technical
      Interview Score >= 7), implemented as an integer 1/0 flag so it can
      be summed directly in analytical queries.
    - YOE_Range: buckets the continuous "years of experience" attribute
      into 5-year ranges, required by Dim_Candidate_Profile (R3) so that
      candidate profiles can be compared as groups rather than as 31
      individual YOE values.
    """
    df = df.copy()

    df["Hired"] = (
        (df["Code Challenge Score"] >= 7) & (df["Technical Interview Score"] >= 7)
    ).astype(int)

    yoe_bins = [-1, 5, 10, 15, 20, 25, 30]
    yoe_labels = ["0-5", "6-10", "11-15", "16-20", "21-25", "26-30"]
    df["YOE_Range"] = pd.cut(df["YOE"], bins=yoe_bins, labels=yoe_labels)

    hired_pct = df["Hired"].mean() * 100
    print(f"[apply_business_rules] Hired: {df['Hired'].sum():,} ({hired_pct:.2f}%)")
    return df


def transform(df: pd.DataFrame) -> pd.DataFrame:
    """Runs the full transform stage: preparation + business rules."""
    df = prepare(df)
    df = apply_business_rules(df)
    return df


if __name__ == "__main__":
    from extract import extract

    raw_df = extract()
    transformed_df = transform(raw_df)
    print(transformed_df[["Application Date", "Seniority", "YOE", "YOE_Range", "Hired"]].head())