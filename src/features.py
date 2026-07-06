"""
features.py

Feature engineering for the IBM AI Enterprise Workflow Capstone.
"""

from pathlib import Path
import pandas as pd


def load_data(filepath):
    """Load cleaned transaction data."""

    df = pd.read_csv(filepath)

    df["invoice_date"] = pd.to_datetime(df["invoice_date"])

    return df


def aggregate_daily(df):
    """Aggregate transactions by day."""

    daily = (
        df.groupby(df["invoice_date"].dt.date)
        .agg(
            revenue=("revenue", "sum"),
            purchases=("invoice", "count"),
            customers=("customer_id", "nunique"),
            views=("times_viewed", "sum"),
        )
        .reset_index()
    )

    daily.rename(
        columns={"invoice_date": "date"},
        inplace=True
    )

    daily["date"] = pd.to_datetime(daily["date"])

    return daily


def create_lag_features(df):

    df["lag_1"] = df["revenue"].shift(1)
    df["lag_7"] = df["revenue"].shift(7)
    df["lag_30"] = df["revenue"].shift(30)

    return df


def create_rolling_features(df):

    df["rolling_7"] = (
        df["revenue"]
        .rolling(window=7)
        .mean()
    )

    df["rolling_30"] = (
        df["revenue"]
        .rolling(window=30)
        .mean()
    )

    return df


def create_calendar_features(df):

    df["day_of_week"] = df["date"].dt.dayofweek
    df["month"] = df["date"].dt.month
    df["quarter"] = df["date"].dt.quarter

    return df


def create_target(df):
    """
    Predict the total revenue over the next 30 days.
    """

    target = []

    revenue = df["revenue"].values

    for i in range(len(df)):

        if i + 30 < len(df):

            target.append(
                revenue[i + 1:i + 31].sum()
            )

        else:

            target.append(None)

    df["target"] = target

    return df


def clean_dataset(df):

    return df.dropna()


def save_features(df, filepath):

    df.to_csv(filepath, index=False)


def build_feature_matrix(input_file, output_file):

    df = load_data(input_file)

    df = aggregate_daily(df)

    df = create_lag_features(df)

    df = create_rolling_features(df)

    df = create_calendar_features(df)

    df = create_target(df)

    df = clean_dataset(df)

    save_features(df, output_file)

    print("\nFeature matrix created successfully!\n")

    print(df.head())


def main():

    root = Path(__file__).resolve().parent.parent

    input_file = root / "data" / "clean_dataset.csv"

    output_file = root / "data" / "features.csv"

    build_feature_matrix(
        input_file,
        output_file
    )


if __name__ == "__main__":
    main()