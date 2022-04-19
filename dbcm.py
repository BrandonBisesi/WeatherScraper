"""Module containing context manager for weather database"""
import sqlite3
import logging

class DBCM:
    """Context manager for weather database"""

    logger = logging.getLogger(f"main.{__name__}")

    def __init__(self):
        """Initializes database context manager."""
        try:
            self.conn = None
            self.cur = None
        except Exception as error:
            self.logger.error("init:%s",error)

    def __enter__(self):
        """Connects to database and returns cursor."""
        try:
            self.conn = sqlite3.connect("weather.sqlite")
            self.cur = self.conn.cursor()
            return self.cur
        except Exception as error:
            self.logger.error("enter:%s",error)

    def __exit__(self, exc_type, exc_value, exc_trace):
        """Closes cursor and connection with database"""
        try:
            self.conn.commit()
            self.cur.close()
            self.conn.close()
        except Exception as error:
            print("exit:%s",error)
