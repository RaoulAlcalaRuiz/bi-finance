from ....models.request.ebitda.ebitda_treatment import EbitdaTreatment
from ....classes.date_delivery import DateDelivery

class EbitdaProvider:
    MONTHS = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12]
    def __init__(self, id_company, year, id_goal, odoo):
        self._year = year
        self._factory_cumulative = EbitdaTreatment(id_company,year,id_goal,odoo,"cumulative")
        self._factory = EbitdaTreatment(id_company,year,id_goal,odoo,"normal")

    def ebitda(self):
        goal = self._factory.get_goal()
        goal_cumulate = self._factory_cumulative.get_goal()
        return [self.MONTHS,goal[0],goal_cumulate[0],goal[1]]


    def null_value_futur(self,list):
        return DateDelivery(list, self._year).new_list