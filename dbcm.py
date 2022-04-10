"""Module containing context manager for weather database"""
import sqlite3
import logging

class DBCM:
    """Context manager for weather database"""

    logger = logging.getLogger(f"main.{__name__}")

    def __init__(self):
        try:
            self.conn = None
            self.cur = None
        except Exception as error:
            self.logger.error(f"DBCM:init:{error}")

    def __enter__(self):
        try:
            self.conn = sqlite3.connect("weather.sqlite")
            self.cur = self.conn.cursor()
            return self.cur
        except Exception as error:
            self.logger.error(f"DBCM:enter:{error}")

    def __exit__(self, exc_type, exc_value, exc_trace):
        try:
            self.conn.commit()
            self.cur.close()
            self.conn.close()
        except Exception as error:
            print(f"DBCM:exit:{error}")