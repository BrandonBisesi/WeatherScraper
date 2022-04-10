
from db_operations import DBOperations
from scrape_weather import WeatherScraper
from plot_operations import PlotOperations
import datetime
import logging

class WeatherProcessor:

    logger = logging.getLogger(f"main.{__name__}")

    def __init__(self,):
        self.db = DBOperations()
        self.db.initialize_db()

    def update(self):
        date = self.db.get_recent_date()
        d = datetime.datetime.strptime(str(date), '%Y-%m-%d')
        month_year = (d.strftime('%B %Y'))
        self.get(month_year)

    def full_update(self):
        self.db.purge_data()
        self.get()

    def get(self, end = None):
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


if __name__ == '__main__':
    try:
        proc = WeatherProcessor()
        while(True):
            prompt = input("Fetch all available weather data, only update existing, or skip? (F)ull/(U)pdate/(S)kip: ")
            if prompt.lower() == "u":
                proc.update()
                break
            elif prompt.lower() == "f":
                proc.full_update()
                break
            elif prompt.lower() == "s":
                break
            else:
                print("Please enter a valid input.")

        run_again = True
        while(run_again):
            p = PlotOperations()
            plot_type = input("Plot monthly or daily data? [M/D]: ")
            if plot_type.lower() == "m":
                try:
                    start_date = input("Enter from year: ")
                    end_date = input("Enter to year: ")
                    p.get_range(int(start_date), int(end_date))
                except ValueError as error:
                    print("Please enter a valid year.")
            elif plot_type.lower() == "d":
                date = input("Please enter a year month in this format YYYY-MM: ")
                p.get_monthly(date)

            while(True):
                finished = input("Finished? [Y/N]: ")
                if finished.lower() == "y":
                    run_again = False
                    break
                elif finished.lower() == "n":
                    break
                else:
                    print("Please enter Y/N")

    except Exception as error:
        proc.logger.error(f"weather_processor:User_input:{error}")