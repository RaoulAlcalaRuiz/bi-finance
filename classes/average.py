from .computer_date import ComputerDate

class Average:
    def __init__(self, first, second):
        self._first = int(first)
        self._second = int(second)
        self._pourcentage = self._compute_pourcentage(self._first,self._second)
        self._pourcentage_formated = self._format_average()

    def _compute_pourcentage(self,first,second):
        if (second == 0) & (first > 0):
            return 100
        elif (second == 0) & (first == 0):
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
