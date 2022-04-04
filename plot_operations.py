from db_operations import DBOperations
import matplotlib.pyplot as plt
from dateutil import parser

class PlotOperations:
    def __init__(self):
        pass

    def get_monthly(self,date):
        results = DBOperations.fetch_data(date)

        mean_temps = [record[5] for record in results]
        timestamps = [parser.parse(record[1]) for record in results]

        plt.plot(timestamps, mean_temps)
        plt.title("Average Daily Temperatures")
        plt.ylabel('Temperature (Celcius)')
        plt.xlabel('Date')
        plt.show()



    def get_range(self, start, end):
        years = range(start,end+1)
        weather_dict = {}

        for month in range(1,13):
            weather_dict[month] = []

        for year in years:
            temps = DBOperations.fetch_data(str(year))
            for temp in temps:
                month = (str((temp[1])[5:7]))

                mean_temp = temp[5]
                weather_dict[int(month)].append(mean_temp)

        data_list = []
        for month in weather_dict:
            spread = list(filter(None,weather_dict[month]))
            data_list.append(spread)
            print(spread)

        plt.boxplot(data_list)
        plt.title(f"Monthly Temperature Distribution for: {start} to {end}")
        plt.ylabel('Temperature (Celcius)')
        plt.xlabel('Month')
        plt.show()


# p = PlotOperations()

# p.get_monthly("2021-12")
# p.get_range(2000,2017)