"""Contains DBOperations class for the database operations in the weather database"""
from dbcm import DBCM

class DBOperations:
    """Database operations for the weather database"""

    @staticmethod
    def fetch_data(date):
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
            print("Error fetching data:", error)
            return None

    @staticmethod
    def save_data(weather_dict):
        """Inserts data into weather table using input dictionary"""
        try:
            with DBCM() as cursor:
                for data in weather_dict:
                    try:
                        sql = """insert into weather (sample_date,location,min_temp,max_temp,avg_temp)
                                    values (?,?,?,?,?)"""
                        values = (data, 'Winnipeg, MB', weather_dict[data]["Min"],
                                    weather_dict[data]["Max"], weather_dict[data]["Mean"])
                        cursor.execute(sql, values)
                    except Exception as error:
                        if str(error) != "UNIQUE constraint failed: weather.sample_date":
                            print("Error inserting data.", error)
        except Exception as error:
            print("Error inserting data:", error)

    @staticmethod
    def initialize_db():
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
            print("Table created successfully.")
        except Exception as error:
            print("Error creating table:", error)

    @staticmethod
    def purge_data():
        """Deletes all data from weather table."""
        try:
            with DBCM() as cursor:
                cursor.execute("""delete from weather""")
        except Exception as error:
            print("Error clearing table:", error)