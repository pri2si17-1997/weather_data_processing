# Weather Data Processing and Ingestion

This repository contains code to process weather data and calculate analytics (average max temperature, avergae min temperature, total precipitation). This is further saved in `SQLite3` database. `Flask` is used to create rest endpoints `/api/weather` and `/api/weather/stats`. `SQLAlchemy` is used to create ORMs.

## Definition of Files

- **`src/data_models.py`**: This module contains ORM data model for weather data.
- **`src/data_ingestion.py`**: This module processes text files and saves data in database.
- **`src/data_metrics_model.py`**: This module contains ORM for data model for weather metrics data.
- **`src/data_metrics_calculation_ingestion.py`**: This module contains code to calculate data anlytics and save it in database.
- **`src/weather_rest_api.py`**: This module contains REST endpoints.

## Instructions to Run

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

## Assumptions and Notes

- No `station` data is provided so, its being ignored while calculating the `data analytics` (calculated on the basis of year only) and creating `REST endpoints` (only date and year are used for filtering and not the station name.)