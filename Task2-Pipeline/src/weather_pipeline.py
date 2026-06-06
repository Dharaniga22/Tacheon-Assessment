# Import Libraries

import requests
import pandas as pd
import logging
from datetime import datetime
from google.cloud import bigquery

# Logging Setup

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)
logging.info("Pipeline started")

# API Parameters

BASE_URL = "https://api.open-meteo.com/v1/forecast"
params = {
    "latitude": 13.0827,   # Chennai
    "longitude": 80.2707,
    "hourly": "temperature_2m,relative_humidity_2m",
    "timezone": "Asia/Kolkata"
}
logging.info("API parameters configured")

# Fetch Data from API

try:
    response = requests.get(BASE_URL, params=params)
    response.raise_for_status()
    data = response.json()
    logging.info("Data fetched successfully from API")

except requests.exceptions.RequestException as e:
    logging.error(f"API request failed: {e}")
    data = None

# Inspect Data Structure

logging.info(f"Available Keys: {list(data.keys())}")
logging.info(f"Hourly Keys: {list(raw_hourly.keys())}")

# Data Transformation - Flattening

df = pd.DataFrame({
    "time": raw_hourly["time"],
    "temperature": raw_hourly["temperature_2m"],
    "humidity": raw_hourly["relative_humidity_2m"]
})
df.head()

# Data Cleaning

df["time"] = pd.to_datetime(df["time"])
df["temperature"] = pd.to_numeric(df["temperature"], errors="coerce")
df["humidity"] = pd.to_numeric(df["humidity"], errors="coerce")
df = df.dropna()
logging.info("Data cleaned successfully")

# Data Quality Validation

logging.info(f"Dataset Shape: {df.shape}")
logging.info(
    f"Missing Values:\n{df.isnull().sum()}"
)
logging.info(
    f"Duplicate Records: {df.duplicated().sum()}"
)
logging.info(
    f"Data Types:\n{df.dtypes}"
)

# Basic validation checks
if df.empty:
    logging.error("Dataset is empty after cleaning")
    raise ValueError("No records available for processing")
logging.info("Data quality checks completed successfully")

# Exploratory Analysis

avg_temp = round(df["temperature"].mean(), 2)
max_temp = round(df["temperature"].max(), 2)
min_temp = round(df["temperature"].min(), 2)
avg_humidity = round(df["humidity"].mean(), 2)
logging.info(
    f"Temperature Summary -> Avg: {avg_temp}°C | "
    f"Min: {min_temp}°C | Max: {max_temp}°C"
)
logging.info(
    f"Average Humidity: {avg_humidity}%"
)
print("\n===== WEATHER DATA SUMMARY =====")
print(df.describe())
print("\n===== TOP 5 HOTTEST HOURS =====")
top_5_hottest = (
    df.sort_values(
        by="temperature",
        ascending=False
    )[["time", "temperature"]]
    .head(5)
)
print(top_5_hottest)
logging.info(
    "EDA completed successfully. Summary statistics and hottest periods identified."
)

# Feature Engineering

df["temp_humidity_index"] = df["temperature"] * (1 - df["humidity"] / 100)
df["hour"] = df["time"].dt.hour
logging.info("Feature engineering completed")

# BiqQuery

PROJECT_ID = "decisive-unison-415017"
DATASET_ID = "weather_dataset"
TABLE_ID = "chennai_weather"
client = bigquery.Client(project=PROJECT_ID)
table_ref = (
    f"{PROJECT_ID}."
    f"{DATASET_ID}."
    f"{TABLE_ID}"
)
job = client.load_table_from_dataframe(
    df,
    table_ref
)
job.result()
print(
    f"Successfully loaded "
    f"{len(df)} rows into BigQuery"
)
logging.info(
    f"Loaded {len(df)} records into {table_ref}"
)
