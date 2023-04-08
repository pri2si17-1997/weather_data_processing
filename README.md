# Weather Data Processing and Ingestion

This repository contains code to process weather data and calculate analytics (average max temperature, avergae min temperature, total precipitation). This is further saved in `SQLite3` database. `Flask` is used to create rest endpoints `/api/weather` and `/api/weather/stats`. `SQLAlchemy` is used to create ORMs.

## Definition of Files

- **`src/data_models.py`**: This module contains ORM data model for weather data.
- **`src/data_ingestion.py`**: This module processes text files and saves data in database.
- **`src/data_metrics_model.py`**: This module contains ORM for data model for weather metrics data.
- **`src/data_metrics_calculation_ingestion.py`**: This module contains code to calculate data anlytics and save it in database.
- **`src/weather_rest_api.py`**: This module contains REST endpoints with swagger documentation.

## Instructions to Run

- Install modules from `requirements.txt`

```bash
python3 -m pip install -r ./requirements.txt
```

- Run `data_ingestion.py`:

```bash
python3 data_ingestion.py --data_path <path/to/wx_data> --db_path <path/to/sqlite3/database.db>
```

- Run `data_metrics_calculation_ingestion.py`:

```bash
python3 data_metrics_calculation_ingestion.py --db_path <path/to/sqlite3/database.db>
```

- Run `weather_rest_api.py`:

```bash
 python3 weather_rest_api.py --db_path <path/to/sqlite3/database.db>
```

This server will start locally on `5000` port. Query string can be passed as:

- http://127.0.0.1:5000/api/weather
- http://127.0.0.1:5000/api/weather/stats
- http://127.0.0.1:5000/api/weather?page=3
- http://127.0.0.1:5000/api/weather?page=1&start_date=2004-01-31
- http://127.0.0.1:5000/api/weather?page=1&start_date=2004-01-31&end_date=2004-02-28
- http://127.0.0.1:5000/api/weather/stats?page=1&year=2004

To view the swagger UI, visit following url:
- http://127.0.0.1:5000/apidocs/

## Development Environment

- Windows 11 with WSL2 (Ubuntu 22.04 LTS, Python 3.10.6, sqlite3 3.37.2)

## Assumptions and Notes

- No `station` data is provided so, its being ignored while calculating the `data analytics` (calculated on the basis of year only) and creating `REST endpoints` (only date and year are used for filtering and not the station name.)

- Its assumed that data is downloaded and sqlite3 is installed in the system.

## Deployment on AWS Suggestions

To deploy the database and API on AWS, following can be used:

- **AWS S3 Bucket**: Text files containing data can be stored on S3 bucket.
- **AWS RDS**: Aamazon RDS can be used to cerate database and communicate with flask API.
- **AWS Lambda**: Lambda function can be used to ingest data from S3 and store it in RDS database. Once that's setup, each time new file is saved in s3 it will trigger the lambda function and database will get updated.
- **AWS API Gateway**: To create and deploy the REST API.
- **AWS CloudWatch**: To monitor performance of the API, logs and resource utilization and set alerts in case of any critical event. 