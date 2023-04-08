"""
data_ingestion.py
=================

This module contains code to ingest data from text files to database.
"""

# Imports
import argparse
import glob2
import os
import sys
import logging

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.exc import IntegrityError
from datetime import datetime

from data_models import Base, WeatherData
from typing import List, Any

def load_data(data_path: str)->List[str]:
    """
    This method reads all text files in the directory:

    Parameters:
        data_path (str): Path of text files.

    Returns:
        text_files (List[str]): List of text files.
    """
    logging.info(f"Path of text files provided : {data_path}")
    text_files = glob2.glob(data_path + '/*.txt')
    return text_files

def parse_data(data_line: str) -> tuple:
    """
    This method parses single tab spaced line and returns required data.

    Parameters:
        data_line (str): Single data line from text file.

    Returns:
        tuple: Tuple containing date, max_temp, min_temp, and precipitation.
    """
    data_split = data_line.strip().split('\t')
    if len(data_split) == 4:
        date = datetime.strptime(data_split[0], "%Y%m%d")
        max_temp = float(data_split[1]) / 10.0
        min_temp = float(data_split[2]) / 10.0
        precipitation = float(data_split[3]) / 10.0
        return (date, max_temp, min_temp, precipitation)
    else:
        logging.error(f"Error: Invalid data {data_line}. Skipping it.")
        return None
    
def data_ingestion_helper(file_path: str, session: Any) -> int:
    """
    This method ingest data from one file. Its being used as an helper method to save all data in database.

    Parameters:
        file_path (str): Path of text file.
        session (Any): SQL Alchemy database session.

    Returns:
        records_ingested (int): Total number of records ingested.
    """
    records_ingested = 0
    with open(file_path, 'r') as fp:
        lines = fp.readlines()
        for line in lines:
            data = parse_data(line)
            if data:
                date, max_temp, min_temp, precipitation = data[0], data[1], data[2], data[3]

                # Check if this record already exists in database.
                existing_record = session.query(WeatherData).filter_by(date=date, max_temp=max_temp, min_temp=min_temp, precipitation=precipitation).first()
                if not existing_record:
                    # Creata new weather data object and save it in database
                    new_record = WeatherData(date=date, max_temp=max_temp, min_temp=min_temp, precipitation=precipitation)
                    session.add(new_record)
                    records_ingested += 1
                else:
                    logging.warning(f"Duplicate record {str(existing_record)} exists for file {file_path}")
    print(f"File processed : {file_path}")

    return records_ingested

def data_ingestion(text_files: List[str], session: Any) -> int:
    """
    This method iterates over each text files and saves data in database using `data_ingestion_helper()` method.

    Parameters:
        text_files (List[str]): List of text files.
        session (Any): SQL Alchemy database session.

    Returns:
        total_records_ingested (int): Number of records saved in database.
    """
    total_records_ingested = 0
    for file_path in text_files:
        records_ingested = data_ingestion_helper(file_path=file_path, session=session)
        total_records_ingested += records_ingested
    return total_records_ingested


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Argumennts to ingest weather data into sqlite3 database.")

    parser.add_argument("-data", "--data_path", type=str, required=True, help="Path of text files.")
    parser.add_argument("-db", "--db_path", type=str, required=True, help="Path of sqlite3 database.")
    args = parser.parse_args()

    # Configure logger.
    logging.basicConfig(filename='weather_data_ingestion.log', level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

    data_path = os.path.abspath(args.data_path)
    if not os.path.exists(data_path):
        logging.error(f"Provided data path {data_path} don't exist. Please provide correct path.")
        sys.exit(0)

    text_files_list = load_data(data_path)
    logging.info(f"Number of text files to ingest : {len(text_files_list)}")
    logging.info(f"Files to ingest : {text_files_list}")

    # Create Database Engine
    engine = create_engine(f'sqlite:///{args.db_path}')
    Session = sessionmaker(bind=engine)
    session = Session()

    # Start connection
    conn = engine.connect()
    logging.info(f"Connection created.")
    
    # Check if table exists
    if not engine.dialect.has_table(conn, WeatherData.__tablename__):
        logging.error(f"Table does not exist : {WeatherData.__tablename__}")
        Base.metadata.create_all(bind=engine)
        logging.info(f"Table created : {WeatherData.__tablename__}")
    
    # Start time
    start_time = datetime.now()
    print(f"Data ingestion started: {start_time.strftime('%Y-%m-%d %H:%M:%S')}")
    logging.info(f"Data ingestion started: {start_time.strftime('%Y-%m-%d %H:%M:%S')}")

    #Ingest files
    records_ingested = data_ingestion(text_files=text_files_list, session=session)

    # Sava data in database.
    # Rollback if error occurs.
    try:
        session.commit()
        print(f"Data Ingestion completed. {records_ingested} record ingested.")
        logging.info(f"Data Ingestion completed. {records_ingested} record ingested.")
    except IntegrityError as ex:
        session.rollback()
        logging.error(f"Error occured while ingestion : {ex}")
    finally:
        session.close()

    # End Time
    end_time = datetime.now()
    elapsed_time = end_time - start_time
    logging.info(f"Data ingestion ended : {end_time.strftime('%Y-%m-%d %H:%M:%S')}")
    logging.info(f"Total time taken : {elapsed_time}")

    # Close the connection
    conn.close()
    logging.info(f"Connection closed")