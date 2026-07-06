# AAVAIL AI Workflow Capstone

## Overview

This project was completed as the IBM AI Enterprise Workflow Capstone.

The objective is to build an end-to-end machine learning system that predicts the next 30 days of revenue for AAVAIL using historical transaction data.

The project follows the complete AI Enterprise Workflow:

- Business Understanding
- Data Ingestion
- Exploratory Data Analysis
- Feature Engineering
- Model Development
- Model Evaluation
- Deployment
- Monitoring
- Unit Testing
- Docker Containerization

---

# Project Structure

```
ai-workflow-capstone/

│
├── app.py
├── run_tests.py
├── requirements.txt
├── Dockerfile
├── docker-compose.yml
│
├── data/
│   ├── clean_dataset.csv
│   └── features.csv
│
├── figures/
│
├── logs/
│
├── models/
│   └── revenue_model.pkl
│
├── src/
│   ├── data_ingestion.py
│   ├── eda.py
│   ├── features.py
│   ├── train_model.py
│   └── predict.py
│
└── tests/
    ├── test_api.py
    ├── test_model.py
    └── test_logging.py
```

---

# Installation

Clone the repository.

```
git clone https://github.com/<username>/ai-workflow-capstone.git

cd ai-workflow-capstone
```

Install dependencies.

```
pip install -r requirements.txt
```

---

# Data Preparation

Run the data ingestion script.

```
python src/data_ingestion.py
```

---

# Exploratory Data Analysis

```
python src/eda.py
```

Generated figures are saved inside the **figures/** directory.

---

# Feature Engineering

```
python src/features.py
```

Creates

```
data/features.csv
```

---

# Train the Model

```
python src/train_model.py
```

Creates

```
models/revenue_model.pkl
```

---

# Make Predictions

```
python src/predict.py
```

---

# Run the Flask API

```
python app.py
```

API runs on

```
http://localhost:5000
```

---

# API Endpoints

## Home

```
GET /
```

Returns API status.

---

## Train

```
POST /train
```

Retrains the model.

---

## Predict

```
POST /predict
```

Example JSON

```json
{
    "country":"United Kingdom",
    "date":"2011-12-01"
}
```

---

## Log File

```
GET /logfile
```

Returns API logs.

---

# Run Unit Tests

Run every test.

```
python run_tests.py
```

or

```
python -m unittest discover tests
```

---

# Docker

Build

```
docker build -t aavail-api .
```

Run

```
docker run -p 5000:5000 aavail-api
```

---

# Models Compared

The following models were evaluated:

- Linear Regression (Baseline)
- Random Forest Regressor
- Gradient Boosting Regressor

The best-performing model is automatically saved for deployment.

---

# Evaluation Metrics

Regression performance is evaluated using:

- RMSE
- MAE

---

# Monitoring

The application logs every prediction request.

Logs are stored in

```
logs/api.log
```

Model performance can be monitored by comparing predicted revenue with actual revenue over time.

---

# Testing

The project includes unit tests for:

- API
- Model
- Logging

All tests can be executed with a single command.

---

# Technologies

- Python
- Flask
- Pandas
- NumPy
- Scikit-learn
- Matplotlib
- Joblib
- Docker
- unittest

---

# Author

Aymen Hajjej

IBM AI Enterprise Workflow Capstone
