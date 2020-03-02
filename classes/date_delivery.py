from datetime import datetime, timedelta


def compute_achievement(reality, goal):
    achievement_list = []
    index = 0
    while index < len(reality) :
        if (reality[index] == 'null') | (goal[index] == 'null'):
            achievement_list.append(True)
        elif float(reality[index]) >= float(goal[index]):
            achievement_list.append(True)
        else:
            achievement_list.append(False)
        index += 1
    return achievement_list


class DateDelivery:
    def __init__(self, list, year):
        self._list = list
        self.year = int(year)
        self.new_list = self._value_null_in_futur()

    def _value_null_in_futur(self):
        today = datetime.today()
        today_month = int(today.month)
        today_year = int(today.year)
        new_list = []
        index = 1
        for value in self._list:
            if today_year < self.year:
                new_list.append('null')
            elif today_year == self.year:
                if today_month < index:
                    new_list.append('null')
                else:
                    new_list.append(value)
            else:
                new_list.append(value)
            index += 1
        return new_list

    def change_list(self,list):
        self._list = list
        self.new_list = self._value_null_in_futur()

class DateDeliveryOne:
    def __init__(self,commitment_date,effective_date,delta):
        self._commitment_date = commitment_date
        self._effective_date = effective_date
        self._delta = delta

    def delivery_in_time(self):
        if self._commitment_date:
            commitment_date = self._commitment_date
            commitment_date = commitment_date - timedelta(days=self._delta)

            if self._effective_date:
                effective_date = self._effective_date
                effective_date = datetime(effective_date.year, effective_date.month, effective_date.day, 0, 0)
                if commitment_date < effective_date:
                    return -1
                else:
                    return 1
            else:
                today = datetime.today()
                if commitment_date < today:
                    return -1
                else:
                    return 0
        else:
            if self._effective_date:
                return 1
            else:
                return 0

