"""
weather_rest_api.py
===================

This module contains REST endpoints to get data from database.
This includes query strings as well.
"""

import argparse
import os

from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy

from data_metrics_model import WeatherStats
from data_models import WeatherData

app = Flask(__name__)


@app.route("/api/weather", methods=["GET"])
def get_weather_data():
    # Since I am not sure of station name as I couldn't find it in data, so not using it for api.
    page = request.args.get("page", 1, type=int)
    start_date = request.args.get("start_date", type=str)
    end_date = request.args.get("end_date", type=str)

    query = db.session.query(WeatherData)

    if start_date:
        query = query.filter(WeatherData.date >= start_date)

    if end_date:
        query = query.filter(WeatherData.date <= end_date)

    results = query.paginate(page=page, per_page=100)
    data = []
    for row in results:
        data.append(
            {
                "id": row.id,
                "date": row.date,
                "max_temp": row.max_temp,
                "min_temp": row.min_temp,
                "precipitation": row.precipitation,
            }
        )

    return jsonify(data)


@app.route("/api/weather/stats", methods=["GET"])
def get_weather_stats_data():
    # Since I am not sure of station name as I couldn't find it in data, so not using it for api.
    page = request.args.get("page", 1, type=int)
    year = request.args.get("year", type=int)

    query = db.session.query(WeatherStats)

    if year:
        query = query.filter(WeatherStats.year == year)

    results = query.paginate(page=page, per_page=10)
    data = []
    for row in results:
        data.append(
            {
                "id": row.id,
                "year": row.year,
                "avg_max_temp": row.avg_max_temp,
                "avg_min_temp": row.avg_min_temp,
                "total_precipitation": row.total_precipitation,
            }
        )
    return jsonify(data)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Argumennts to analyse data and save it in database."
    )

    parser.add_argument(
        "-db", "--db_path", type=str, required=True, help="Path of sqlite3 database."
    )
    args = parser.parse_args()

    db_path = os.path.abspath(args.db_path)

    # Configure flask app.
    app.config["SQLALCHEMY_DATABASE_URI"] = f"sqlite:///{db_path}"
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

    db = SQLAlchemy(app)
    app.run(debug=True)
