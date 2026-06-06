# Task 2: Data Pipeline – Open-Meteo Weather Data to BigQuery

## Overview

This project demonstrates a complete data pipeline that extracts weather data from a public API, transforms and enriches the data, and loads it into Google BigQuery for analysis.

The objective of this task was to simulate a real-world data engineering workflow where external data is automatically collected, processed, stored, and made available for reporting.

## API Chosen

### Open-Meteo API

I selected the Open-Meteo API because:

* It is publicly available and free to use.
* No API key is required.
* It provides structured JSON responses.
* The data contains nested fields that require transformation.
* It is suitable for demonstrating extraction, transformation, and loading (ETL) concepts.

API Endpoint:

https://api.open-meteo.com/v1/forecast

## Pipeline Architecture

Open-Meteo API → Python Pipeline → Data Transformation → BigQuery → SQL Analysis

## Features Implemented

### Data Extraction

* Retrieves hourly weather data for Chennai.
* Uses parameterized API requests.
* Handles API failures using exception handling.
* Includes logging for monitoring execution.

### Data Transformation

The raw API response is transformed into a tabular structure containing:

* time
* temperature
* humidity

Data cleaning includes:

* Datetime conversion
* Numeric type conversion
* Null value handling
* Basic data validation

### Feature Engineering

A derived metric was created:

temp_humidity_index

Formula:

`temperature × (1 - humidity / 100)`

This provides an additional analytical indicator beyond the raw API response.

### Data Quality Checks

The pipeline validates:

* Dataset shape
* Missing values
* Duplicate records
* Data types

### BigQuery Loading

Processed data is loaded into:

Project:
decisive-unison-415017

Dataset:
weather_dataset

Table:
chennai_weather

## Project Structure

```text
Task2-Pipeline/
│
├── Images/
│   ├── bigquery_table_preview.png
│   ├── sql_query_results.png
│   ├── pipeline_architecture.png
│   ├── flow_diagram.png
│
├── README.md
├── Walkthrough.md
│
├── sql/
│   └── weather_summary.sql
│
└── src/
    └── weather_pipeline.py
```

## How to Run

Install dependencies:

`pip install requests pandas google-cloud-bigquery pyarrow`

Run the pipeline:

python src/pipeline.py

The script will:

1. Fetch data from Open-Meteo.
2. Transform and clean the data.
3. Generate derived features.
4. Load the final dataset into BigQuery.

## SQL Summary Query

The following query identifies average temperature and humidity by hour:

```sql
SELECT
hour,
ROUND(AVG(temperature), 2) AS avg_temperature,
ROUND(AVG(humidity), 2) AS avg_humidity
FROM `decisive-unison-415017.weather_dataset.chennai_weather`
GROUP BY hour
ORDER BY avg_temperature DESC;
```

### Sample Insight

The query shows which hours of the day experience the highest average temperatures and how humidity changes throughout the day.

Screenshot:

See images/sql_query_results.png

## Production Considerations

### How would this pipeline be scheduled?

In production, I would schedule the pipeline using:

* Apache Airflow
* Cloud Scheduler
* Cron Jobs

A daily execution schedule would be sufficient for this dataset.

### How would failures be detected?

Failures could be monitored through:

* Application logs
* Email alerts
* Cloud Monitoring dashboards
* Pipeline execution status checks

### How would the pipeline scale to 10× data volume?

For larger data volumes, I would:

* Implement incremental loading.
* Partition BigQuery tables by date.
* Use batch processing.
* Add retry mechanisms.
* Store raw and transformed data separately.
* Introduce orchestration using Airflow.

## Conclusion

This project demonstrates a complete ETL pipeline using Python, Open-Meteo, and BigQuery. The solution includes data extraction, transformation, validation, feature engineering, cloud storage, and analytical querying while following basic data engineering best practices.
