"""Module containing WeatherProcessor class and user interface."""
import datetime
import logging
from db_operations import DBOperations
from scrape_weather import WeatherScraper
from plot_operations import PlotOperations

class WeatherProcessor:
    """Weather Processor class for using the WeatherScraper and DBOperations"""

    def __init__(self):
        self.db = DBOperations()
        self.db.initialize_db()
        self.logger = logging.getLogger(__name__)
        self.logger.info("Weather Processor Started")

    def prompt_user(self):
        """Prompt user and uses prompt for weather processor."""
        try:
            while True:
                try:
                    prompt = input("Fetch all available weather data, only update existing, or skip? (F)ull/(U)pdate/(S)kip: ")
                    if prompt.lower() == "u":
                        self.update()
                        break
                    elif prompt.lower() == "f":
                        self.full_update()
                        break
                    elif prompt.lower() == "s":
                        break
                    else:
                        print("Please enter a valid input.")
                except Exception as error:
                    self.logger.error("prompt_user:fetch/update/skip:%s",error)

            run_again = True
            while run_again:
                try:
                    plot = PlotOperations()
                    while True:
                        try:
                            plot_type = input("Plot monthly or daily data? [M/D]: ")
                            if plot_type.lower() == "m":
                                try:
                                    start_date = input("Enter from year: ")
                                    end_date = input("Enter to year: ")
                                    plot.get_range(int(start_date), int(end_date))
                                    break
                                except ValueError:
                                    print("Please enter a valid year.")
                            elif plot_type.lower() == "d":
                                date = input("Please enter a year month in this format YYYY-MM: ")
                                plot.get_monthly(date)
                                break
                            else:
                                print("Please enter M/D")

                        except Exception as error:
                            self.logger.error("monthly/daily:%s",error)

                    while True:
                        finished = input("Finished? [Y/N]: ")
                        if finished.lower() == "y":
                            run_again = False
                            self.logger.info("Weather Processor Ended")
                            break
                        elif finished.lower() == "n":
                            break
                        else:
                            print("Please enter Y/N")

                except Exception as error:
                    self.logger.error("User_input:%s",error)

        except Exception as error:
            self.logger.error("User_input:%s",error)

    def update(self):
        """Calls the get method with the most recent date in the db."""
        try:
            recent_date = self.db.get_recent_date()
            d = datetime.datetime.strptime(str(recent_date), '%Y-%m-%d')
            month_year = (d.strftime('%B %Y'))
            self.get(month_year)
        except Exception as error:
            self.logger.error("update:%s",error)

    def full_update(self):
        """Purges the db then call the get method."""
        try:
            self.db.purge_data()
            self.get()
        except Exception as error:
            self.logger.error("full_update:%s",error)

    def get(self, end = None):
        """Gets all the data using the WeatherScraper and saves it to the db."""
        try:
            today = datetime.datetime.today()
            year = int(today.year)
            month = int(today.month)
            more_data = True

            while(more_data):
                while month > 0:
                    weather_scraper = WeatherScraper()
                    month_date = datetime.date(year, month, 1).strftime('%B %Y')
                    print("Checking", month_date)
                    self.db.save_data(weather_scraper.get_weather(month,year))

                    if weather_scraper.end_of_dates or month_date == end:
                        print("---No more data---")
                        more_data = False
                        break
                    month -= 1
                year -= 1
                month = 12

        except Exception as error:
            self.logger.error("get:%s",error)

def main_log():
    """Creates the logger."""
    try:
        logging.basicConfig(format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", filename='file.log')
        logger = logging.getLogger(__name__)
        logger.setLevel(logging.DEBUG)

        logger.info("Main Started")

        proc = WeatherProcessor()
        proc.prompt_user()

    except Exception as error:
        logger.error("main_log:%s",error)

if __name__ == '__main__':
    main_log()
