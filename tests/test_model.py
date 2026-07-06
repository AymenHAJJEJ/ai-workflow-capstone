"""
test_model.py

Unit tests for the trained revenue prediction model.
"""

import unittest
import joblib
import pandas as pd
import os


MODEL_PATH = "models/revenue_model.pkl"
FEATURES_PATH = "data/features.csv"


class TestRevenueModel(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        """Load model and sample data once."""

        cls.model = joblib.load(MODEL_PATH)

        df = pd.read_csv(FEATURES_PATH)

        cls.X = df.drop(
            columns=["date", "target"],
            errors="ignore"
        )

    def test_model_exists(self):
        """Model file should exist."""

        self.assertTrue(os.path.exists(MODEL_PATH))

    def test_prediction(self):
        """Model should return one prediction."""

        prediction = self.model.predict(self.X.iloc[:1])

        self.assertEqual(len(prediction), 1)

    def test_prediction_numeric(self):
        """Prediction should be numeric."""

        prediction = self.model.predict(self.X.iloc[:1])[0]

        self.assertIsInstance(
            float(prediction),
            float
        )

    def test_multiple_predictions(self):
        """Model should predict multiple rows."""

        predictions = self.model.predict(self.X.iloc[:10])

        self.assertEqual(len(predictions), 10)


if __name__ == "__main__":
    unittest.main()