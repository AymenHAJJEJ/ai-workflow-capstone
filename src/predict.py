"""
predict.py

Load the trained model and predict revenue.
"""

from pathlib import Path
import joblib
import pandas as pd

ROOT = Path(__file__).resolve().parent.parent

MODEL_PATH = ROOT / "models" / "revenue_model.pkl"


def load_model():
    return joblib.load(MODEL_PATH)


def prepare_input(features_file, country=None):

    df = pd.read_csv(features_file)

    if country is not None and "country" in df.columns:

        df = df[df["country"] == country]

        if df.empty:
            raise ValueError(f"No data found for '{country}'.")

    latest = df.tail(1)

    X = latest.drop(
        columns=["date", "target", "country"],
        errors="ignore"
    )

    return X


def predict(features_file, country=None):

    model = load_model()

    X = prepare_input(features_file, country)

    return model.predict(X)[0]


def main():

    features = ROOT / "data" / "features.csv"

    prediction = predict(features)

    print(prediction)


if __name__ == "__main__":
    main()