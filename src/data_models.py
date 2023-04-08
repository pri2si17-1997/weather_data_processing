"""
data_models.py
==============

This module contains data model for weather data and its metric.
"""

from datetime import datetime

# Imports
from sqlalchemy import Column, Date, Float, Integer
from sqlalchemy.orm import declarative_base

Base = declarative_base()


class WeatherData(Base):
    """
    Represents a table in a database that stores weather data.

    Attributes:
    -----------
    __tablename__ : str
        The name of the table in the database.
    id : int
        The primary key of the table.
    date : datetime.date
        The date of the weather data.
    max_temp : float
        The maximum temperature recorded for the date.
    min_temp : float
        The minimum temperature recorded for the date.
    precipitation : float
        The amount of precipitation recorded for the date.
    """

    __tablename__ = "weather_data"

    id = Column(Integer, primary_key=True)
    date = Column(Date)
    max_temp = Column(Float)
    min_temp = Column(Float)
    precipitation = Column(Float)

    def __init__(
        self, date: datetime, max_temp: float, min_temp: float, precipitation: float
    ) -> None:
        """
        Constructs a WeatherData object.

        Parameters:
        -----------
        date : datetime.date
            The date of the weather data.
        max_temp : float
            The maximum temperature recorded for the date.
        min_temp : float
            The minimum temperature recorded for the date.
        precipitation : float
            The amount of precipitation recorded for the date.
        """

        self.date = date
        self.max_temp = max_temp
        self.min_temp = min_temp
        self.precipitation = precipitation
