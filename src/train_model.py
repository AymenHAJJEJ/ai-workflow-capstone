"""
train_model.py

Train and compare multiple machine learning models for
the AAVAIL AI Workflow Capstone.
"""

from pathlib import Path

import joblib
import pandas as pd

from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error, mean_absolute_error

from sklearn.linear_model import LinearRegression
from sklearn.ensemble import RandomForestRegressor, GradientBoostingRegressor


ROOT = Path(__file__).resolve().parent.parent

MODEL_PATH = ROOT / "models" / "revenue_model.pkl"
FEATURE_PATH = ROOT / "data" / "features.csv"


def load_features(filepath):
    """
    Load engineered feature dataset.
    """

    df = pd.read_csv(filepath)

    # Remove non-feature columns if present
    X = df.drop(
        columns=["date", "target", "country"],
        errors="ignore"
    )

    y = df["target"]

    return X, y


def evaluate(model, X_test, y_test):

    predictions = model.predict(X_test)

    rmse = mean_squared_error(
        y_test,
        predictions,
        squared=False
    )

    mae = mean_absolute_error(
        y_test,
        predictions
    )

    return rmse, mae


def compare_models(X_train, X_test, y_train, y_test):

    models = {
        "Linear Regression":
            LinearRegression(),

        "Random Forest":
            RandomForestRegressor(
                n_estimators=200,
                random_state=42
            ),

        "Gradient Boosting":
            GradientBoostingRegressor(
                random_state=42
            )
    }

    best_model = None
    best_rmse = float("inf")

    for name, model in models.items():

        model.fit(X_train, y_train)

        rmse, mae = evaluate(
            model,
            X_test,
            y_test
        )

        print(f"\n{name}")
        print(f"RMSE : {rmse:.2f}")
        print(f"MAE  : {mae:.2f}")

        if rmse < best_rmse:
            best_rmse = rmse
            best_model = model

    return best_model


def save_model(model):

    MODEL_PATH.parent.mkdir(
        exist_ok=True
    )

    joblib.dump(
        model,
        MODEL_PATH
    )

    print("\nModel saved to")

    print(MODEL_PATH)


def main():

    X, y = load_features(FEATURE_PATH)

    X_train, X_test, y_train, y_test = train_test_split(
        X,
        y,
        test_size=0.20,
        shuffle=False,
        random_state=42
    )

    best_model = compare_models(
        X_train,
        X_test,
        y_train,
        y_test
    )

    best_model.fit(X, y)

    save_model(best_model)


if __name__ == "__main__":
    main()