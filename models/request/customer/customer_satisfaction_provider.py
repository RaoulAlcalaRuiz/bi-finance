from ....classes.date_delivery import DateDelivery, compute_achievement_list
from ....models.request.customer.customer_satisfaction_treatment import CustomerSatisfactionTreatment


class CustomerSatisfactionProvider:
    MONTHS = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12]
    def __init__(self, id_company, year, id_goal, odoo):
        self._year = year
        self._factory = CustomerSatisfactionTreatment(id_company,year,id_goal,odoo)

    def delivery_in_time(self):
        result = self._factory.get_result_otd()
        result_otd = self.null_value_futur(result[0])
        result_accrued_otd = self.null_value_futur(result[1])
        goal = self._factory.get_goal_otd()
        goal_achieved = compute_achievement_list(result_otd,goal)
        return [
                (self.MONTHS,result_otd,result_accrued_otd,goal),
                (self.MONTHS,[self._formated_all_percent(result_otd),goal_achieved],self._formated_all_percent(result_accrued_otd),self._formated_all_percent(goal))
                ]

    def quality(self):
        result = self._factory.get_result_oqd()
        result_oqd = self.null_value_futur(result[0])
        result_accrued_oqd = self.null_value_futur(result[1])
        goal = self._factory.get_goal_oqd()
        goal_achieved = compute_achievement_list(result_oqd,goal)
        return [
                (self.MONTHS, result_oqd, result_accrued_oqd, goal),
                (self.MONTHS, [self._formated_all_percent(result_oqd),goal_achieved], self._formated_all_percent(result_accrued_oqd), self._formated_all_percent(goal))
                ]

    def null_value_futur(self,list):
        return DateDelivery(list, self._year).new_list

    def _formated_all_percent(self, list):
        new_list = []
        for value in list:
            if value != 'null' :
                new_list.append(self._format_percent(value))
            else:
                new_list.append('-')
        return new_list

    def _format_percent(self, value):
        return "{:4.1f} %".format(value)


