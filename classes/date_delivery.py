from datetime import datetime, timedelta
from ..library.business_calendar.business_calendar.business_calendar  import Calendar, MO, TU, WE, TH, FR

def compute_achievement_list(reality, goal):
    achievement_list = []
    index = 0
    while index < len(reality) :
        achievement_list.append(compute_achievement(reality[index],goal[index]))
        index += 1
    return achievement_list

def compute_achievement(reality, goal):
    if (reality == 'null') | (goal == 'null'):
        return True
    elif float(reality) >= float(goal):
        return True
    else:
        return False

def _value_null_in_futur( value, year, real_year, month, real_month):
    year = int(year)
    real_year = int(real_year)
    month = int(month)
    real_month = int(real_month)
    if real_year < year:
        return 'null'
    elif real_year == year:
        if real_month < month:
            return 'null'
        else:
            return value
    else:
        return value

# [(effective,commitment),...]
def on_time_business_day_list(list, time_delivery):
    count = 0
    for delivery in list:
        if on_time_business_day(delivery[0],delivery[1],time_delivery):
            count = 1 + count
    return count

def on_time_business_day (effective, commitment,time_delivery):
    cal = Calendar(workdays=[MO, TU, WE, TH, FR])
    return cal.busdaycount(effective, commitment) >= time_delivery

class DateDelivery:
    def __init__(self, list, year):
        self._list = list
        self.year = int(year)
        self.new_list = self._value_null_in_futur_list()

    def _value_null_in_futur_list(self):
        today = datetime.today()
        today_month = int(today.month)
        today_year = int(today.year)
        new_list = []
        index = 1
        for value in self._list:
            new_list.append(_value_null_in_futur(value,self.year,today_year,index,today_month))
            index += 1
        return new_list

    def change_list(self,list):
        self._list = list
        self.new_list = self._value_null_in_futur_list()

class DateDeliveryOne:
    def __init__(self,commitment_date,effective_date,delta):
        self._commitment_date = commitment_date
        self._effective_date = effective_date
        self._delta = delta

    def delivery_in_time(self):
        if self._commitment_date:
            commitment_date = self._commitment_date

            if self._effective_date:
                effective_date = self._effective_date
                effective_date = datetime(effective_date.year, effective_date.month, effective_date.day, 0, 0)
                commitment_date = datetime(commitment_date.year, commitment_date.month, commitment_date.day, 0, 0)
                if on_time_business_day(effective_date,commitment_date,self._delta):
                    return 1
                else:
                    return -1
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

