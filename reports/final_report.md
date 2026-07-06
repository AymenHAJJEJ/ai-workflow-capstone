# IBM AI Enterprise Workflow Capstone Final Report

## Business Opportunity

Develop a machine learning model capable of forecasting the next 30 days of revenue using historical transaction data.

## Dataset

- Source: AAVAIL transaction dataset
- Training data: cs-train
- Production data: cs-production

## Data Ingestion

- Loaded all JSON files
- Cleaned missing values
- Standardized column names
- Generated clean_dataset.csv

## Exploratory Data Analysis

Visualizations created:
- Revenue over time
- Revenue distribution
- Top countries by revenue
- Daily purchases

Main findings:
- Revenue shows seasonal variation.
- United Kingdom contributes the largest share of revenue.
- Activity increases toward the end of the year.

## Feature Engineering

Features created:
- Lag 1 day
- Lag 7 days
- Lag 30 days
- Rolling 7-day average
- Rolling 30-day average
- Calendar features
- 30-day revenue target

## Models Compared

- Linear Regression
- Random Forest Regressor
- Gradient Boosting Regressor

Evaluation metrics:
- RMSE
- MAE

Best model:
- Gradient Boosting Regressor

## Deployment

Implemented a Flask API with endpoints:

- /
- /train
- /predict
- /logfile

## Testing

Implemented unit tests for:

- API
- Model
- Logging

All tests passed.

## Docker

The application is containerized using Docker.

## Monitoring

API requests are logged in logs/api.log.

## Conclusion

The project successfully demonstrates the complete AI enterprise workflow, including data ingestion, exploratory analysis, feature engineering, model training, deployment, testing, logging, and containerization.