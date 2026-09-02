"""
extract.py
Task 3.1 - Extract

Reads the raw source file and loads it into a Pandas DataFrame.
No business transformations are performed here - this stage only
gets the data into memory exactly as it exists in the source file.
The original source file is preserved untouched in data/raw/.
"""

import pandas as pd

RAW_DATA_PATH = "data/raw/candidates.csv"


def extract(path: str = RAW_DATA_PATH) -> pd.DataFrame:
    """
    Read the raw candidates CSV file (semicolon-delimited) into a
    Pandas DataFrame. The source file is never modified or overwritten.
    """
    df = pd.read_csv(path, sep=";")
    print(f"[extract] Loaded {len(df):,} rows and {len(df.columns)} columns from {path}")
    return df


if __name__ == "__main__":
    raw_df = extract()
    print(raw_df.head())