from datetime import datetime
import calendar


def leap_year(year):
    return int(year) % 4 == 0


class ComputerDate:
    def __init__(self, month, year):
        self.month = int(month)
        self.year = int(year)

    # Return le nombre de jour d'un mois, valeur : 28-31
    def day_of_month(self):
        return calendar.monthrange(self.year, self.month)[1]

    # Return 0 ou (28-29-30-31) ou le jour de la date d'aujourd'hui
    def real_day_of_month(self):
        today = datetime.today()
        real_year = int(today.year)
        real_month = int(today.month)

        if self.year == real_year:
            if real_month == self.month:
                return today.day
            if real_month > self.month:
                return self.get_day_month_range()
            else:
                return 0
        if self.year < real_year:
            return self.get_day_month_range()
        else:
            return 0

    def day_of_year(self):
        real_year = int(datetime.today().year)

        if self.year == real_year:
            return datetime.now().timetuple().tm_yday
        if self.year < real_year:
            if leap_year(self.year):
                return 366
            else:
                return 365
        else:
            return 0

    # return 365 or 366
    def get_day_year_range(self):
        if leap_year(self.year):
            return 366
        else:
            return 365

    # return 28-29-30-31
    def get_day_month_range(self):
        return calendar.monthrange(self.year, self.month)[1]
