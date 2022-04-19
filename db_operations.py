"""Contains DBOperations class for the database operations in the weather database"""
import logging
from dbcm import DBCM

class DBOperations:
    """Database operations for the weather database"""

    def __init__(self):
        self.logger = logging.getLogger(f"main.{__name__}")

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
            self.logger.error("DBOperations:fetch_data:%s",error)
            return None

    def fetch_range(self,start_year, end_year):
        """Fetch data from weather table using the data."""
        try:
            result = None
            with DBCM() as cursor:
                sql = """select * from weather where sample_date BETWEEN ? and ?"""
                values = (start_year,end_year)
                cursor.execute(sql,values)
                result = cursor.fetchall()
            return tuple(result)
        except Exception as error:
            self.logger.error("DBOperations:fetch_data:%s",error)
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
                        self.logger.error("DBOperations:save_data:%s:%s",data,error)
        except Exception as error:
            self.logger.error("DBOperations:save_data:%s",error)

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
            self.logger.error("DBOperations:initialize_db:%s",error)

    def purge_data(self):
        """Deletes all data from weather table."""
        try:
            with DBCM() as cursor:
                cursor.execute("""delete from weather""")
        except Exception as error:
            self.logger.error("DBOperations:purge_data:%s",error)


    def get_recent_date(self):
        """Get most recent date in database."""
        try:
            with DBCM() as cursor:
                cursor.execute("""select max(sample_date) from weather""")
                date = cursor.fetchone()
                return date[0]
        except Exception as error:
            self.logger.error("DBOperations:get_recent_date:%s",error)
