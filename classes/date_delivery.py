from datetime import datetime


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

