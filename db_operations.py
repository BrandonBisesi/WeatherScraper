
from dbcm import DBCM
import datetime
from scrape_weather import WeatherScraper
class DBOperations:

  def fetch_data(self):
    pass

  def save_data(self, weather_dict):
    with DBCM() as cursor:
      for data in weather_dict:
        try:
          sql = """insert into weather (sample_date,location,min_temp,max_temp,avg_temp)
                      values (?,?,?,?,?)"""
          values = (data, 'Winnipeg, MB', weather_dict[data]["Min"], weather_dict[data]["Max"], weather_dict[data]["Mean"])
          cursor.execute(sql, values)
        except Exception as e:
          # if str(e) != "UNIQUE constraint failed: weather.sample_date":
            print("Error inserting sample.", e)

  def initialize_db(self):
    try:
      with DBCM() as cursor:
        cursor.execute("""drop table weather""")
        cursor.execute("""create table if not exists weather
                        (id integer primary key autoincrement not null,
                        sample_date text unique not null,
                        location text,
                        min_temp real,
                        max_temp real,
                        avg_temp real);""")
        print("Table created successfully.")
    except Exception as e:
        print("Error creating table:", e)

  def purge_data(self):
    pass


today = datetime.datetime.today()
year = int(today.year)
month = int(today.month)

db = DBOperations()

db.initialize_db()
more_data = True
while more_data:
  while month > 0:
    weather_scraper = WeatherScraper()
    month_date = datetime.date(year, month, 1).strftime('%B %Y')
    print("Checking", month_date)
    db.save_data(weather_scraper.get_weather(month,year))

    if weather_scraper.end_of_dates:
      print("---No more data---")
      more_data = False
      break
    month -= 1
  year -= 1
  month = 12


