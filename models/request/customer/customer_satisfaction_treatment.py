from .customer_satisfaction_sql import CustomerSatisfactionSql
from ....classes.result_interpretation import ResultInterpretationZero

class CustomerSatisfactionTreatment:
    def __init__(self,id_company,year,id_goal,odoo):
        self._sql = CustomerSatisfactionSql(id_company,year,id_goal,odoo)
        self._interpretation = ResultInterpretationZero()

    # Time Request
    def get_goal_otd(self):
        goal_otd = []
        for i in range(1, 13):
            month_result = self.month_goal_otd(i)
            goal_otd.append(month_result)
        return goal_otd

    def get_result_otd(self):
        result_otd = []
        result_cumulative_otd = []
        in_time_cumulative = 0
        all_cumulative = 0
        for i in range(1, 13):
            month_result = self.month_result_otd(i)
            in_time_cumulative += month_result[0]
            all_cumulative += month_result[1]
            average_otd = self._average_delivery(month_result[0], month_result[1])
            average_cumulative_otd = self._average_delivery(month_result[0], month_result[1])
            result_otd.append(average_otd)
            result_cumulative_otd.append(average_cumulative_otd)
        return [result_otd,result_cumulative_otd]

    def month_goal_otd(self, month):
        self.change_month(month)
        result_sql = self._sql.get_goal_otd()
        return self.interpretation(result_sql)

    def month_result_otd(self,month):
        self.change_month(month)
        time_delivery = self.interpretation(self._sql.get_time_delivery())
        in_time = self.interpretation(self._sql.get_count_month_delivery_in_time(time_delivery))
        all_delivery = self.interpretation(self._sql.get_count_month_delivery())
        return (in_time,all_delivery)

    # Quality Request
    def get_goal_oqd(self):
        goal_oqd = []
        for i in range(1, 13):
            month_result = self.month_goal_oqd(i)
            goal_oqd.append(month_result)
        return goal_oqd

    def get_result_oqd(self):
        result_oqd = []
        result_cumulative_oqd = []
        good_quality_cumulative = 0
        all_cumulative = 0
        for i in range(1, 13):
            month_result = self.month_result_oqd(i)
            good_quality_cumulative += month_result[0]
            all_cumulative += month_result[1]

            average_oqd = self._average_delivery(month_result[0], month_result[1])
            average_cumulative_oqd = self._average_delivery(month_result[0], month_result[1])

            result_oqd.append(average_oqd)
            result_cumulative_oqd.append(average_cumulative_oqd)
        return [result_oqd,result_cumulative_oqd]

    def month_goal_oqd(self, month):
        self.change_month(month)
        result_sql = self._sql.get_goal_oqd()
        return self.interpretation(result_sql)

    def month_result_oqd(self,month):
        self.change_month(month)
        good_quality = self.interpretation(self._sql.get_quality_delivery("False"))
        all_quality = self.interpretation(self._sql.get_quality_delivery("True")) + good_quality
        return (good_quality,all_quality)

    # Generics
    def change_month(self,month):
        self._sql.set_month(month)

    def format_month(self,month):
        return "{:02d}".format(month)

    def interpretation(self,result):
        return self._interpretation.interpretation(result)

    def _average_delivery(self, in_time, count):
        result = 0
        if count == 0:
            if (count == 0 & in_time != 0):
                result = 100
        else:
            result = in_time / count * 100
        return result

