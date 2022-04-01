"""Module containing HTMLParser for getting the all the daily weather from climate.weather.gc.ca"""
from html.parser import HTMLParser
import urllib.request
from datetime import datetime

class WeatherScraper(HTMLParser):
  """HTML Parser to get the daily weather from climate.weather.gc.ca"""
  title_flag = False
  row_flag = False
  date_flag = False
  temp_flag = False
  count = 0
  max = 0
  min = 0
  mean = 0
  month_year = ""
  date = ""
  weather = {}

  def handle_starttag(self, tag, attrs):
    try:
      if self.date_flag and tag == "td" and self.count<=3:
        self.temp_flag = True
        self.count += 1

      for attr in attrs:
        try:
          if tag == "h1":
            if "id" in attr and "wb-cont" in attr:
              self.title_flag = True
          if "scope" in attr and "row" in attr:
            self.row_flag = True
          if self.row_flag and "title" in attr:
            if str(attr[1]) != "Average" and str(attr[1]) != "Extreme":
              d = datetime.strptime(str(attr[1]), '%B %d, %Y')
              self.date = (d.strftime('%Y-%m-%d'))
              self.date_flag = True

        except Exception as e:
            print("Error reading attribute of start tag", e)
    except Exception as e:
        print("Error reading start tag", e)

  def handle_data(self, data):
    try:
      if self.title_flag:
        self.month_year = str(data[22:])
        self.title_flag = False
      if self.temp_flag:
        daily_temps = {}
        if self.count == 1:
          self.max = float(data)
          self.temp_flag = False
        elif self.count == 2:
          self.min = float(data)
          self.temp_flag = False
        elif self.count == 3:
          self.mean = float(data)
          self.temp_flag = False

          daily_temps["Max"] = self.max
          daily_temps["Min"] = self.min
          daily_temps["Mean"] = self.mean
          self.weather[self.date] = daily_temps

          self.temp_flag = False
          self.date_flag = False
          self.count = 0

    except Exception as e:
        print("Error reading data", e)


weather_scraper = WeatherScraper()

with urllib.request.urlopen('https://climate.weather.gc.ca/climate_data/daily_data_e.html?StationID=27174&timeframe=2&StartYear=1840&EndYear=2018&Day=1&Year=2022&Month=3#') as response:
    html = str(response.read())

# weather_scraper.feed(html)
# # print(weather_scraper.month_year)
# # print(weather_scraper.weather)

