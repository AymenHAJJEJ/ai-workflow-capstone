"""
ingest.py

IBM AI Enterprise Workflow Capstone

Reads every JSON file from the training and production
directories, cleans the data and saves a single dataset.
"""

from pathlib import Path
import json
import pandas as pd


# ---------------------------------------------------------
# Column Standardization
# ---------------------------------------------------------

def standardize_columns(df):

    mapping = {
        "Invoice": "invoice",
        "InvoiceNo": "invoice",

        "CustomerID": "customer_id",
        "Customer ID": "customer_id",

        "Country": "country",

        "Price": "price",
        "price": "price",

        "TotalPrice": "total_price",
        "total_price": "total_price",

        "StreamID": "stream_id",
        "stream_id": "stream_id",

        "TimesViewed": "times_viewed",
        "times_viewed": "times_viewed",

        "Year": "year",
        "Month": "month",
        "Day": "day",
    }

    df.rename(columns=mapping, inplace=True)

    return df


# ---------------------------------------------------------
# Invoice Cleaning
# ---------------------------------------------------------

def clean_invoice(invoice):

    invoice = str(invoice)

    invoice = invoice.replace("C", "")
    invoice = invoice.replace("A", "")

    return invoice.strip()


# ---------------------------------------------------------
# Read One JSON File
# ---------------------------------------------------------

def load_json(filepath):

    try:

        with open(filepath, "r", encoding="utf-8") as f:

            data = json.load(f)

        return pd.DataFrame(data)

    except Exception as e:

        print(f"Could not read {filepath}")

        print(e)

        return pd.DataFrame()


# ---------------------------------------------------------
# Clean DataFrame
# ---------------------------------------------------------

def clean_dataframe(df):

    df = standardize_columns(df)

    required = [
        "country",
        "customer_id",
        "invoice",
        "stream_id",
        "times_viewed",
        "year",
        "month",
        "day",
    ]

    missing = [c for c in required if c not in df.columns]

    if missing:
        raise ValueError(f"Missing required columns: {missing}")

    # Clean invoice
    df["invoice"] = df["invoice"].apply(clean_invoice)

    # Revenue
    if "total_price" in df.columns:
        df["revenue"] = pd.to_numeric(
            df["total_price"],
            errors="coerce"
        )
    elif "price" in df.columns:
        df["revenue"] = pd.to_numeric(
            df["price"],
            errors="coerce"
        )
    else:
        raise ValueError(
            "Neither 'price' nor 'total_price' found."
        )

    # Numeric columns
    df["times_viewed"] = pd.to_numeric(
        df["times_viewed"],
        errors="coerce"
    )

    # Create date
    df["invoice_date"] = pd.to_datetime(
        dict(
            year=df["year"],
            month=df["month"],
            day=df["day"]
        ),
        errors="coerce"
    )

    # Remove bad rows
    df.dropna(
        subset=[
            "invoice_date",
            "revenue"
        ],
        inplace=True
    )

    df.drop_duplicates(inplace=True)

    df.sort_values(
        "invoice_date",
        inplace=True
    )

    df.reset_index(
        drop=True,
        inplace=True
    )

    return df


# ---------------------------------------------------------
# Load Dataset
# ---------------------------------------------------------

def load_dataset():

    root = Path(__file__).resolve().parent.parent

    folders = [
        root / "cs-train",
        root / "cs-production",
    ]

    files = []

    for folder in folders:

        files.extend(sorted(folder.glob("*.json")))

    if not files:
        raise FileNotFoundError(
            "No JSON files found."
        )

    print(f"\nFound {len(files)} JSON files.\n")

    dfs = []

    for file in files:

        print(f"Reading {file.name}")

        df = load_json(file)

        if df.empty:
            continue

        df = clean_dataframe(df)

        dfs.append(df)

    dataset = pd.concat(
        dfs,
        ignore_index=True
    )

    dataset.sort_values(
        "invoice_date",
        inplace=True
    )

    dataset.reset_index(
        drop=True,
        inplace=True
    )

    return dataset


# ---------------------------------------------------------
# Save Dataset
# ---------------------------------------------------------

def save_dataset(df):

    root = Path(__file__).resolve().parent.parent

    output_dir = root / "data"

    output_dir.mkdir(
        exist_ok=True
    )

    output_file = output_dir / "clean_dataset.csv"

    df.to_csv(
        output_file,
        index=False
    )

    print(f"\nDataset saved to:\n{output_file}")


# ---------------------------------------------------------
# Main
# ---------------------------------------------------------

def main():

    print("\nLoading dataset...\n")

    df = load_dataset()

    print("\nDataset Shape:")
    print(df.shape)

    print("\nColumns:")
    print(df.columns.tolist())

    print("\nFirst Five Rows:")
    print(df.head())

    print("\nSummary:")
    print(df.describe(include="all"))

    save_dataset(df)


if __name__ == "__main__":
    main()