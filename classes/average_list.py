from .average import Average
from .computer_date import ComputerDate

class AverageList:
    def __init__(self, list, list_goal):
        self._list = list
        self._list_goal = list_goal

    def compute_average(self, year):
        new_list = []
        i = 0
        while i < len(self._list):
            if (self._list[i] != "null") & (self._list_goal[i] != 'null'):
                average = Average(self._list[i], self._list_goal[i])
                c_d = ComputerDate(i + 1, year)
                days = c_d.day_of_month()
                real_days = c_d.real_day_of_month()
                new_list.append([average.get_pourcentage_formated(),
                                 average.compute_in_time_average(real_days, days)
                                 ])
            elif (self._list[i] == "null") & (self._list_goal[i] != 'null'):
                new_list.append([self.percent_format(0), False])
            elif (self._list[i] != "null") & (self._list_goal[i] == 'null'):
                new_list.append([self.percent_format(100), True])
            else:
                new_list.append([self.percent_format(0), True])
            i += 1
        return new_list

    def percent_format(self,value):
        return "{:4.1f} %".format(value)
