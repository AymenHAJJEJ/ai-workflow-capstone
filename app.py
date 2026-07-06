"""
app.py

Flask API for the AAVAIL AI Workflow Capstone.
"""

import os
import logging
import subprocess

from flask import Flask, request, jsonify

from src.predict import predict

app = Flask(__name__)

LOG_FILE = "logs/api.log"

os.makedirs("logs", exist_ok=True)

logging.basicConfig(
    filename=LOG_FILE,
    level=logging.INFO,
    format="%(asctime)s %(levelname)s %(message)s"
)


@app.route("/")
def home():
    return jsonify({
        "message": "AAVAIL Revenue Prediction API",
        "status": "running"
    })


@app.route("/train", methods=["POST"])
def train():

    try:

        subprocess.run(
            ["python", "src/train_model.py"],
            check=True
        )

        logging.info("Model retrained successfully.")

        return jsonify({
            "status": "success",
            "message": "Model retrained successfully."
        })

    except Exception as e:

        logging.error(str(e))

        return jsonify({
            "status": "error",
            "message": str(e)
        }), 500


@app.route("/predict", methods=["POST"])
def predict_endpoint():

    data = request.get_json(silent=True)

    if not data:

        return jsonify({
            "error": "JSON input required."
        }), 400

    if "date" not in data:

        return jsonify({
            "error": "Missing required field: date"
        }), 400

    country = data.get("country", None)

    try:

        revenue = predict(
            "data/features.csv",
            country
        )

        logging.info(
            f"Prediction requested for {country}"
        )

        return jsonify({

            "country": country if country else "ALL",

            "date": data["date"],

            "predicted_30_day_revenue":
                round(float(revenue), 2)

        })

    except Exception as e:

        logging.error(str(e))

        return jsonify({
            "error": str(e)
        }), 500


@app.route("/logfile", methods=["GET"])
def logfile():

    if not os.path.exists(LOG_FILE):

        return jsonify({
            "message": "Log file does not exist."
        })

    with open(LOG_FILE, "r") as file:

        content = file.readlines()

    return jsonify(content)


if __name__ == "__main__":

    app.run(
        host="0.0.0.0",
        port=5000,
        debug=True
    )