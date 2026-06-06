# Walkthrough – Task 2 Data Pipeline



## Introduction



The goal of this task was to build a complete data pipeline using a public API and load the transformed data into BigQuery.



Rather than focusing only on data extraction, I approached the task as a simplified version of a real-world ETL workflow.



## Why I Chose Open-Meteo



I selected the Open-Meteo API because it is publicly accessible, reliable, and provides structured weather data without requiring authentication.



The API response contains nested JSON data, making it suitable for demonstrating data transformation and cleaning.



## Extraction Approach



The pipeline begins by calling the Open-Meteo API using Python's requests library.



To make the solution more robust, I added:



* Parameterized API requests

* Exception handling

* Logging statements



This helps ensure that failures can be detected and diagnosed easily.



## Transformation Decisions



The API returns hourly weather data in nested structures.



I converted the response into a pandas DataFrame and extracted:



* Time

* Temperature

* Humidity



After flattening the data, I performed:



* Datetime conversion

* Numeric conversion

* Null handling

* Validation checks



This ensures the final dataset is suitable for analysis.



## Feature Engineering



I wanted to add analytical value beyond simply storing raw API data.



For this reason, I created a derived field called:



temp\_humidity\_index



This metric combines temperature and humidity information into a single indicator.



Although simple, it demonstrates how raw data can be enhanced before storage.



## BigQuery Design



BigQuery was selected because it was explicitly required by the assessment.



I created:



Dataset:

weather\_dataset



Table:

chennai\_weather



The transformed DataFrame is loaded directly into BigQuery using the Google Cloud BigQuery Python client.



## SQL Analysis



After loading the data, I created a SQL query to summarize average temperature and humidity by hour.



This demonstrates that the data is not only stored successfully but is also queryable and useful for reporting.



## What I Would Improve With More Time



If more time were available, I would:



* Add configuration files for parameters.

* Create automated unit tests.

* Add retry logic for API failures.

* Implement incremental data loading.

* Add dashboard visualizations.

* Schedule the pipeline using Airflow.



## Final Thoughts



My focus throughout this task was to build a practical and maintainable pipeline rather than a highly complex solution.



The final result demonstrates the complete ETL process: extracting data from an external source, transforming it into a usable format, loading it into BigQuery, and generating meaningful analytical outputs through SQL.



