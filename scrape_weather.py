"""Module containing HTMLParser for getting the all the daily weather from climate.weather.gc.ca"""
from html.parser import HTMLParser
import urllib.request
import datetime
import logging

class WeatherScraper(HTMLParser):
    """HTML Parser to get the daily weather from climate.weather.gc.ca"""

    def __init__(self):
        """Initialize the web scraper"""
        try:
            super().__init__()
            self.end_of_dates = False
            self.title_flag = False
            self.row_flag = False
            self.date_flag = False
            self.temp_flag = False
            self.count = 0
            self.max = 0
            self.min = 0
            self.mean = 0
            self.input = ""
            self.date = ""
            self.weather = {}
            self.logger = logging.getLogger(f"main.{__name__}")
        except Exception as error:
            self.logger.error("init:%s",error)

    def handle_starttag(self, tag, attrs):
        """Handles start tags of the web scraper"""
        try:
            if not self.end_of_dates:
                if tag == "h1":
                    self.title_flag = True

                if self.date_flag and tag == "td" and self.count<=3:
                    self.temp_flag = True
                    self.count += 1
                for attr in attrs:
                    try:
                        if "scope" in attr and "row" in attr:
                            self.row_flag = True

                        if self.row_flag and "title" in attr:
                            if str(attr[1]) != "Average" and str(attr[1]) != "Extreme" and str(attr[1]) != "Sum":
                                try:
                                    d = datetime.datetime.strptime(str(attr[1]), '%B %d, %Y')
                                    self.date = (d.strftime('%Y-%m-%d'))
                                    self.date_flag = True
                                except Exception as error:
                                    self.logger.error("handle_starttag:error_getting_date: %s",error)
                            self.row_flag = False

                    except Exception as error:
                        print("handle_starttag:%s:%s",attr,error)
        except Exception as error:
            self.logger.error("handle_starttag:%s",error)

    def handle_data(self, data):
        """Handles data of the web scraper"""
        try:
            if self.title_flag:
                month_year = str(data[22:])
                if month_year != self.input:
                    self.end_of_dates = True
                self.title_flag = False
            if self.temp_flag:
                daily_temps = {}
                if self.count == 1:
                    self.temp_flag = False
                    try:
                        self.max = float(data)
                    except ValueError:
                        self.max = None
                elif self.count == 2:
                    self.temp_flag = False
                    try:
                        self.min = float(data)
                    except ValueError:
                        self.min = None
                elif self.count == 3:
                    self.temp_flag = False
                    self.date_flag = False
                    self.count = 0
                    try:
                        self.mean = float(data)
                    except ValueError:
                        self.mean = None

                    daily_temps["Max"] = self.max
                    daily_temps["Min"] = self.min
                    daily_temps["Mean"] = self.mean
                    self.weather[self.date] = daily_temps

        except Exception as error:
            self.logger.error("handle_data:%s",error)

    def get_weather(self,month,year):
        """Gets the weatherfrom climate.weather.gc.ca using the input month and year"""
        try:
            self.input = datetime.date(year, month, 1).strftime('%B %Y')
            with urllib.request.urlopen(f'https://climate.weather.gc.ca/climate_data/daily_data_e.html?StationID=27174&timeframe=2&StartYear=1840&EndYear=2022&Day=1&Year={year}&Month={month}#') as response:
                html = str(response.read())
            self.feed(html)
            return self.weather
        except Exception as error:
            self.logger.error("get_weather:%s",error)
