from .computer_date import ComputerDate


# =============  AverageList Class  =============
class AverageList:
    def __init__(self, list):
        self._list = list

    def sum_data(self):
        sum_data = 0
        for r in self._list:
            if len(r) != 0:
                sum_data += r[0][0]
        return sum_data

    def cumulative_data(self,stop):
        new_list = []
        cumulative_data = 0
        for r in self._list:
            if len(r) != 0:
                cumulative_data += r[0][0]
                new_list.append(cumulative_data)
            else:
                if stop:
                    if self.data_continue(len(new_list)):
                        new_list.append(cumulative_data)
                    else:
                        new_list.append('null')
                else:
                    new_list.append(cumulative_data)
        return new_list

    def data_continue(self, i):
        index_null = 0
        index = i
        while i < len(self._list):
            if len(self._list[i]) == 0:
                index_null += 1
            i += 1
        return not(index_null+index == len(self._list))

    def compute_average(self, year, list_goal):
        new_list = []
        average = 0
        i = 0
        while i < len(self._list):
            if (self._list[i] != "null") & (list_goal[i] != 'null'):
                average = Average(self._list[i], list_goal[i])
                c_d = ComputerDate(i + 1, year)
                days = c_d.day_of_month()
                real_days = c_d.real_day_of_month()
                new_list.append([average.get_pourcentage_formated(),
                                 average.compute_in_time_average(real_days, days)
                                 ])
            elif (self._list[i] == "null") & (list_goal[i] != 'null'):
                new_list.append(["{:4.1f} %".format(0), False])
            elif (self._list[i] != "null") & (list_goal[i] == 'null'):
                new_list.append(["{:4.1f} %".format(100), True])
            else:
                new_list.append(["{:4.1f} %".format(0), True])
            i += 1
        return new_list

# =============  Average Class  =============
class Average:
    def __init__(self, first, second):
        self._first = int(first)
        self._second = int(second)
        self._pourcentage = self._compute_pourcentage(self._first,self._second)
        self._pourcentage_formated = self._format_average()

    def _compute_pourcentage(self,first,second):
        if second == 0 & first < 0:
            return 100
        elif second == 0 & first == 0:
            return 0
        else:
            return first / second * 100

    def _format_average(self):
        return "{:4.1f} %".format(self._pourcentage)

    def compute_in_time_average(self, day_now, days):
        return self._compute_pourcentage(day_now, days) <= self._pourcentage

    def compute_in_time_average_year(self, year):
        c_d = ComputerDate(1, year)
        total_days = c_d.get_day_year_range()
        now_day_year = c_d.day_of_year()
        return self._compute_pourcentage(now_day_year, total_days) <= self._pourcentage

    def get_pourcentage(self):
        return self._pourcentage

    def get_pourcentage_formated(self):
        return self._pourcentage_formated
