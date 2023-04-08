"""
data_metrics_model.py
=====================

This module contains data model for weather analytics.
"""

# Imports
from sqlalchemy import Column, Float, Integer
from sqlalchemy.orm import declarative_base

Base = declarative_base()


class WeatherStats(Base):
    """
    Represents a table in a database that stores weather data metrics.

    Attributes:
    -----------
    __tablename__ : str
        The name of the table in the database.
    id : int
        The primary key of the table.
    year : int
        Year of aggregate data.
    avg_max_temp : float
        Average max temperature for the year.
    avg_min_temp : float
        Average min temperature for the year.
    total_precipitation : float
        Total precipitation for the year.
    """

    __tablename__ = "weather_stats"
    id = Column(Integer, primary_key=True)
    year = Column(Integer)
    # station = Column(String)
    # We don't have station column in given data and neither the separation of files are provided.
    # So skipping this field. But if we have station data, we can add a column as mentioned above.
    avg_max_temp = Column(Float)
    avg_min_temp = Column(Float)
    total_precipitation = Column(Float)

    def __init__(
        self,
        year: int,
        avg_max_temp: float,
        avg_min_temp: float,
        total_precipitation: float,
    ) -> None:
        """
        Constructs a WeatherStats object.

        Parameters:
        -----------
        year : int
            The year of the aggregate weather data.
        avg_max_temp : float
            Average max temperature for the year.
        avg_min_temp : float
            Average min temperature for the year.
        total_precipitation : float
            Total precipitation for the year.
        """

        self.year = year
        self.avg_max_temp = avg_max_temp
        self.avg_min_temp = avg_min_temp
        self.total_precipitation = total_precipitation
