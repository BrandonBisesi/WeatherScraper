"""Contains DBOperations class for the database operations in the weather database"""
from dbcm import DBCM
import logging
import datetime
from scrape_weather import WeatherScraper

class DBOperations:
    """Database operations for the weather database"""

    logger = logging.getLogger(f"main.{__name__}")

    def fetch_data(self, date):
        """Fetch data from weather table using the data."""
        try:
            result = None
            with DBCM() as cursor:
                sql = """select * from weather where sample_date like ?"""
                values = (date+'%',)
                cursor.execute(sql,values)
                result = cursor.fetchall()
            return tuple(result)
        except Exception as error:
            self.logger.error(f"DBOperations:fetch_data:{error}")
            return None

    def save_data(self, weather_dict):
        """Inserts data into weather table using input dictionary"""
        try:
            with DBCM() as cursor:
                for data in weather_dict:
                    try:
                        sql = """insert or ignore into weather (sample_date,location,min_temp,max_temp,avg_temp)
                                    values (?,?,?,?,?)"""
                        values = (data, 'Winnipeg, MB', weather_dict[data]["Min"],
                                    weather_dict[data]["Max"], weather_dict[data]["Mean"])
                        cursor.execute(sql, values)
                    except Exception as error:
                        print("Error inserting data.", error)
                        self.logger.error(f"DBOperations:save_data:{data}:{error}")
        except Exception as error:
            self.logger.error(f"DBOperations:save_data:{error}")

    def initialize_db(self):
        """Initializes weather table."""
        try:
            with DBCM() as cursor:
                cursor.execute("""create table if not exists weather
                                (id integer primary key autoincrement not null,
                                sample_date text unique not null,
                                location text,
                                min_temp real,
                                max_temp real,
                                avg_temp real);""")
        except Exception as error:
            self.logger.error(f"DBOperations:initialize_db:{error}")

    def purge_data(self):
        """Deletes all data from weather table."""
        try:
            with DBCM() as cursor:
                cursor.execute("""delete from weather""")
        except Exception as error:
            self.logger.error(f"DBOperations:purge_data:{error}")


    def get_recent_date(self):
        """Get most recent date in database."""
        try:
            with DBCM() as cursor:
                cursor.execute("""select max(sample_date) from weather""")
                date = cursor.fetchone()
                return date[0]
        except Exception as error:
            self.logger.error(f"DBOperations:get_recent_date:{error}")