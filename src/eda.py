"""
eda.py

Exploratory Data Analysis for the AAVAIL Capstone.
Generates summary statistics and visualizations.
"""

import os
import pandas as pd
import matplotlib.pyplot as plt


FIGURES_DIR = "../figures"


def create_output_directory():
    """Create the figures directory if it doesn't exist."""
    os.makedirs(FIGURES_DIR, exist_ok=True)


def load_data(filepath):
    """Load the cleaned dataset."""
    df = pd.read_csv(filepath)
    df["invoice_date"] = pd.to_datetime(df["invoice_date"])
    return df


def dataset_summary(df):
    """Print dataset information."""
    print("\n========== DATASET INFO ==========\n")
    print(df.info())

    print("\n========== SUMMARY ==========\n")
    print(df.describe(include="all"))

    print("\n========== MISSING VALUES ==========\n")
    print(df.isnull().sum())


def revenue_by_day(df):
    """Daily revenue time series."""

    daily = (
        df.groupby(df["invoice_date"].dt.date)["revenue"]
        .sum()
        .reset_index()
    )

    plt.figure(figsize=(12, 6))
    plt.plot(daily["invoice_date"], daily["revenue"])
    plt.title("Daily Revenue")
    plt.xlabel("Date")
    plt.ylabel("Revenue")
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.savefig(f"{FIGURES_DIR}/daily_revenue.png")
    plt.close()


def top_countries(df):
    """Top 10 countries by revenue."""

    revenue = (
        df.groupby("country")["revenue"]
        .sum()
        .sort_values(ascending=False)
        .head(10)
    )

    plt.figure(figsize=(10, 6))
    revenue.plot(kind="bar")
    plt.title("Top 10 Countries by Revenue")
    plt.xlabel("Country")
    plt.ylabel("Revenue")
    plt.tight_layout()
    plt.savefig(f"{FIGURES_DIR}/top_countries.png")
    plt.close()


def purchases_per_day(df):
    """Number of purchases each day."""

    purchases = (
        df.groupby(df["invoice_date"].dt.date)
        .size()
    )

    plt.figure(figsize=(12, 6))
    plt.plot(purchases.index, purchases.values)
    plt.title("Purchases Per Day")
    plt.xlabel("Date")
    plt.ylabel("Purchases")
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.savefig(f"{FIGURES_DIR}/purchases_per_day.png")
    plt.close()


def missing_values(df):
    """Visualize missing values."""

    missing = df.isnull().sum()

    plt.figure(figsize=(8, 5))
    missing.plot(kind="bar")
    plt.title("Missing Values")
    plt.ylabel("Count")
    plt.tight_layout()
    plt.savefig(f"{FIGURES_DIR}/missing_values.png")
    plt.close()


def monthly_revenue(df):
    """Monthly revenue trend."""

    monthly = (
        df.groupby(df["invoice_date"].dt.to_period("M"))["revenue"]
        .sum()
    )

    plt.figure(figsize=(12, 6))
    monthly.plot()
    plt.title("Monthly Revenue")
    plt.xlabel("Month")
    plt.ylabel("Revenue")
    plt.tight_layout()
    plt.savefig(f"{FIGURES_DIR}/monthly_revenue.png")
    plt.close()


def run_eda(filepath):
    """Run all EDA steps."""

    create_output_directory()

    df = load_data(filepath)

    dataset_summary(df)

    revenue_by_day(df)

    top_countries(df)

    purchases_per_day(df)

    monthly_revenue(df)

    missing_values(df)

    print("\nEDA completed successfully.")
    print(f"Figures saved in '{FIGURES_DIR}'.")


def main():

    data_file = "../data/clean_dataset.csv"

    run_eda(data_file)


if __name__ == "__main__":
    main()