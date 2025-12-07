"""
data_cleaning.py
----------------
This script loads a messy sales dataset. It performs data-cleaning steps,
and writes the final result in data/processed/. It produces a
clean CSV file.
"""
import pandas as pd

# Copilot-assisted function
# This function loads a CSV file 
# Keeps file loading separate for easy testing.

def load_data(file_path: str) -> pd.DataFrame:
    """Load the raw sales data from the given file path."""
    df = pd.read_csv(file_path)
    return df


# Copilot-assisted function
# This function standardizes column names by making it lowercase and replacing spaces with underscores
# Clean column names make analysis easier.

def clean_column_names(df: pd.DataFrame) -> pd.DataFrame:
    df = df.copy()
    df.columns = (
        df.columns.str.strip()
        .str.lower()
        .str.replace(" ", "_")
        .str.replace("-", "_")
    )
    return df


# Clean text fields
# Strip extra spaces in product/category
# Leading and trailing spaces are common errors

def strip_text_fields(df: pd.DataFrame) -> pd.DataFrame:
    df = df.copy()
    text_cols = df.select_dtypes(include=["object"]).columns
    for col in text_cols:
        df[col] = df[col].astype(str).str.strip()
    return df


# Handle missing values
# Fills missing quantities with 0 and missing prices with 0.
# For this assignment consistency matters most.

def handle_missing_values(df: pd.DataFrame) -> pd.DataFrame:
    df = df.copy()
    if "quantity" in df.columns:
        df["quantity"] = df["quantity"].fillna(0)

    if "price" in df.columns:
        df["price"] = df["price"].fillna(0)

    return df



# Removes invalid rows
# Removes rows where quantity or price is negative.
# Negative values are clearly data-entry errors for this dataset.

def remove_invalid_rows(df: pd.DataFrame) -> pd.DataFrame:
    df = df.copy()

    if "quantity" in df.columns:
        df = df[df["quantity"] >= 0]

    if "price" in df.columns:
        df = df[df["price"] >= 0]

    return df


# Final
# Runs only when executing the script directly.
# It loads, cleans, removes errors, saves cleaned CSV.

if __name__ == "__main__":
    raw_path = "data/raw/sales_data_raw.csv"
    cleaned_path = "data/processed/sales_data_clean.csv"

    # Load the raw data
    df_raw = load_data(raw_path)

    # Run cleaning steps
    df_clean = clean_column_names(df_raw)
    df_clean = strip_text_fields(df_clean)
    df_clean = handle_missing_values(df_clean)
    df_clean = remove_invalid_rows(df_clean)

    # Save the cleaned data
    df_clean.to_csv(cleaned_path, index=False)

    print("Cleaning complete. First few rows:")
    print(df_clean.head())