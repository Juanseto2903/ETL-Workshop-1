# ---
# jupyter:
#   jupytext:
#     cell_metadata_filter: -all
#     formats: ipynb,py:light
#     text_representation:
#       extension: .py
#       format_name: light
#       format_version: '1.5'
#       jupytext_version: 1.19.5
# ---

"""
Task 1 - Initial Data Profiling
ETL (G01) - Workshop 1
Recruitment candidates dataset
"""

import pandas as pd

# --- Extract (no business transformations here) ---
df = pd.read_csv('data/raw/candidates.csv', sep=';')

# --- Structure ---
print("Shape (rows, columns):", df.shape)
print("\nColumn names:")
print(df.columns.tolist())
print("\nData types:")
print(df.dtypes)

# --- Missing values ---
print("\nMissing values per column:")
print(df.isnull().sum())

# --- Duplicates ---
print("\nFully duplicated rows:", df.duplicated().sum())
print("Duplicate emails:", df['Email'].duplicated().sum())
print("Duplicate (First Name + Last Name + Email):",
      df.duplicated(subset=['First Name', 'Last Name', 'Email']).sum())

# --- Categorical attributes ---
print("\nUnique countries:", df['Country'].nunique())
print("\nSeniority value counts:")
print(df['Seniority'].value_counts())
print("\nUnique technologies:", df['Technology'].nunique())
print(sorted(df['Technology'].unique()))

# --- Application Date ---
df['Application Date'] = pd.to_datetime(df['Application Date'], errors='coerce')
print("\nMin application date:", df['Application Date'].min())
print("Max application date:", df['Application Date'].max())
print("Invalid/unparseable dates:", df['Application Date'].isnull().sum())

# --- Numeric ranges & descriptive statistics ---
print("\nYOE descriptive statistics:")
print(df['YOE'].describe())

print("\nScore descriptive statistics:")
print(df[['Code Challenge Score', 'Technical Interview Score']].describe())

print("\nOut-of-range scores (expected 0-10):")
print("Code Challenge Score:",
      ((df['Code Challenge Score'] < 0) | (df['Code Challenge Score'] > 10)).sum())
print("Technical Interview Score:",
      ((df['Technical Interview Score'] < 0) | (df['Technical Interview Score'] > 10)).sum())

# --- Hiring business rule (for profiling purposes only; official
#     transformation happens in Task 3 - Business Transformation) ---
hired = (df['Code Challenge Score'] >= 7) & (df['Technical Interview Score'] >= 7)
print("\nHired candidates:", hired.sum(), f"({hired.mean() * 100:.2f}%)")
print("Not hired candidates:", (~hired).sum(), f"({(~hired).mean() * 100:.2f}%)")
