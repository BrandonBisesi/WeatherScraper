"""Module containing a class for plotting weather data."""
import logging
import matplotlib.pyplot as plt
from dateutil import parser
from db_operations import DBOperations

class PlotOperations:
    """Class to create plots for weather data."""

    def __init__(self):
        self.logger = logging.getLogger(f"main.{__name__}")

    def get_monthly(self,date):
        """Creates a plot for a month of weather data."""
        try:
            db = DBOperations()
            results = db.fetch_data(date)

            mean_temps = [record[5] for record in results]
            timestamps = [parser.parse(record[1]) for record in results]

            plt.plot(timestamps, mean_temps)
            plt.title(f"Average Daily Temperatures for {date}")
            plt.ylabel('Temperature (Celcius)')
            plt.xlabel('Date')
            self.logger.info("Open Plot")
            plt.show()
        except Exception as error:
            self.logger.error("PlotOperations:get_monthly:%s",error)

    def get_range(self, start_year, end_year):
        """Creates a box plot for years of weather data."""
        try:
            weather_dict = {}
            db = DBOperations()
            for month in range(1,13):
                weather_dict[month] = []

            temps = db.fetch_range(start_year, end_year)

            for temp in temps:
                try:
                    month = (str((temp[1])[5:7]))
                    mean_temp = temp[5]
                    weather_dict[int(month)].append(mean_temp)

                except Exception as error:
                    self.logger.error("PlotOperations:get_range:month %s:%s",month,error)


            data_list = []
            for month in weather_dict:
                spread = list(filter(None,weather_dict[month]))
                data_list.append(spread)

            plt.boxplot(data_list)
            plt.title(f"Monthly Temperature Distribution for: {start_year} to {end_year}")
            plt.ylabel('Temperature (Celcius)')
            plt.xlabel('Month')
            self.logger.info("Open Box Plot")
            plt.show()

        except Exception as error:
            self.logger.error("PlotOperations:get_range:%s",error)
