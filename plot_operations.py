"""Module containing a class for plotting weather data."""
from db_operations import DBOperations
import matplotlib.pyplot as plt
from dateutil import parser
import logging

class PlotOperations:
    """Class to create plots for weather data."""
    logger = logging.getLogger(f"main.{__name__}")

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
            plt.show()
        except Exception as error:
            self.logger.error(f"PlotOperations:get_monthly:{error}")

    def get_range(self, start_year, end_year):
        """Creates a box plot for years of weather data."""
        try:
            years = range(start_year,end_year+1)
            weather_dict = {}
            db = DBOperations()
            for month in range(1,13):
                weather_dict[month] = []

            for year in years:
                try:
                    temps = db.fetch_data(str(year))

                    for temp in temps:
                        try:
                            month = (str((temp[1])[5:7]))
                            mean_temp = temp[5]
                            weather_dict[int(month)].append(mean_temp)

                        except Exception as error:
                            self.logger.error(f"PlotOperations:get_range:month {month}:{error}")

                except Exception as error:
                    self.logger.error(f"PlotOperations:get_range:year {year}:{error}")


            data_list = []
            for month in weather_dict:
                spread = list(filter(None,weather_dict[month]))
                data_list.append(spread)

            plt.boxplot(data_list)
            plt.title(f"Monthly Temperature Distribution for: {start_year} to {end_year}")
            plt.ylabel('Temperature (Celcius)')
            plt.xlabel('Month')
            plt.show()

        except Exception as error:
            self.logger.error(f"PlotOperations:get_range:{error}")