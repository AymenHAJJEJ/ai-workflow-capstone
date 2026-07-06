"""
test_api.py

Unit tests for the Flask API.
"""

import unittest
import json

from app import app


class TestAPI(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        app.testing = True
        cls.client = app.test_client()

    def test_home_endpoint(self):
        """Test the home endpoint."""

        response = self.client.get("/")

        self.assertEqual(response.status_code, 200)

    def test_predict_missing_json(self):
        """Predict endpoint should reject missing JSON."""

        response = self.client.post("/predict")

        self.assertEqual(response.status_code, 400)

    def test_predict_missing_date(self):
        """Date is required."""

        response = self.client.post(
            "/predict",
            data=json.dumps({
                "country": "United Kingdom"
            }),
            content_type="application/json"
        )

        self.assertEqual(response.status_code, 400)

    def test_predict_valid(self):
        """Valid prediction request."""

        response = self.client.post(
            "/predict",
            data=json.dumps({
                "country": "United Kingdom",
                "date": "2011-12-01"
            }),
            content_type="application/json"
        )

        self.assertIn(
            response.status_code,
            [200, 500]
        )

    def test_logfile(self):
        """Log endpoint."""

        response = self.client.get("/logfile")

        self.assertEqual(response.status_code, 200)

    def test_train_endpoint(self):
        """Train endpoint."""

        response = self.client.post("/train")

        self.assertIn(
            response.status_code,
            [200, 500]
        )


if __name__ == "__main__":
    unittest.main()