"""Module containing context manager for weather database"""
import sqlite3

class DBCM:
    """Context manager for weather database"""
    def __init__(self):
        try:
            self.conn = sqlite3.connect("weather.sqlite")
            self.cur = self.conn.cursor()
        except Exception as error:
            print("Error connecting to DB.", error)

    def __enter__(self):
        return self.cur

    def __exit__(self, exc_type, exc_value, exc_trace):
        try:
            self.conn.commit()
            self.cur.close()
            self.conn.close()
        except Exception as error:
            print("Error closing DB connection.", error)