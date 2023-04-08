"""
data_metrics_calculation_ingestion.py
=====================================

This module contains code to fetch weather data records and calculate relevant analytics and save it to the database.
"""
from data_metrics_model import Base, WeatherStats
from data_models import WeatherData
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from typing import Any

import argparse

import pandas as pd

def get_weather_data(session: Any)->pd.DataFrame:
    """
    This method fetches weather data from WeatherData model and returns pandas dataframe.
    Pandas dataframe can be useful to calculate aggregate metrics.

    Parameters:
        session (Any): SQL Alchemy session
    
    Returns:
        result_df (pd.DataFrame): Pandas dataframe containing weather data records.
    """
    results = session.query(WeatherData).all()
    result_df = pd.DataFrame([r.__dict__ for r in results])
    result_df = result_df.drop(['_sa_instance_state', 'id'], axis = 1)
    result_df.date = pd.to_datetime(result_df.date)
    result_df['year'] = result_df.date.dt.year
    return result_df

def calculate_analytics(result_df:pd.DataFrame)->pd.DataFrame:
    """
    This method calculates the aggreagte metrics on weather data.
    Pandas dataframe is used to groupby data by year and calculate aggregate metrics.

    Parameters:
        result_df (pd.DataFrame): Records from weather data.

    Returns:
        result_df_grouped (pd.DataFrame): Aggregate stats for weather data.
    """
    result_df_grouped = result_df.groupby('year').agg({'max_temp': 'mean', 'min_temp': 'mean', 'precipitation': 'sum'})
    result_df_grouped = result_df_grouped.rename(columns={'max_temp': 'avg_max_temp', 'min_temp': 'avg_min_temp', 'precipitation': 'total_precipitation'})
    result_df_grouped = result_df_grouped.reset_index()
    return result_df_grouped

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Argumennts to analyse data and save it in database.")

    parser.add_argument("-db", "--db_path", type=str, required=True, help="Path of sqlite3 database.")
    args = parser.parse_args()

    # Create Database Engine
    engine = create_engine(f'sqlite:///{args.db_path}')
    Session = sessionmaker(bind=engine)
    session = Session()

    # Start connection
    conn = engine.connect()
    
    # Check if weather stats table exists
    if not engine.dialect.has_table(conn, WeatherStats.__tablename__):
        Base.metadata.create_all(bind=engine)

    # Fetch weather data.
    weather_data_df = get_weather_data(session=session)
    # print(f"Weather Data:")
    # print(weather_data_df.head())

    # Calcualte Analytics.
    result_df_grouped = calculate_analytics(weather_data_df)
    result_df_grouped_dict = result_df_grouped.to_records(index=False)
    
    #print(result_df_grouped_dict)

    # Iterate and save in database.
    for item in result_df_grouped_dict:
        year = int(item[0])
        avg_max_temp = item[1]
        avg_min_temp = item[2]
        total_precipitation = item[3]
        weather_stats_data  = WeatherStats(
            year=year,
            avg_max_temp=avg_max_temp,
            avg_min_temp=avg_min_temp,
            total_precipitation=total_precipitation
        )
        session.add(weather_stats_data)
        session.commit()
    
    # Close connection.
    session.close()
    conn.close()