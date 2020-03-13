from ...classes.average import Average
from ...classes.average_list import AverageList
from ..request.sale_order_treatment import SaleOrderTreatment


class SaleOrderProvider:
    MONTHS = [1,2,3,4,5,6,7,8,9,10,11,12]

    def __init__(self, year, odoo, treatment):
        self._year = year
        self._factory = SaleOrderTreatment(year,odoo,treatment)

    # [months,Resultats,Objectifs,[réaliser, indicateur],[total_resultat,total_objectif,[total_réaliser, indicateur]]]
    def annual_sales(self):
        sales = self._factory.annual_sales()
        goal = self._factory.annual_sales_goal()
        average = self.average(sales[0],goal[0])
        return [self.MONTHS,
                sales[0],
                goal[0],
                average,
                [sales[1],goal[1],self.average_year(sales[1],goal[1],self._year)]]

    def average(self,real,goal):
        return AverageList(real,goal).compute_average(self._year)

    def average_year(self,real,goal,year):
        av = Average(real, goal)
        return [av.get_pourcentage_formated(),av.compute_in_time_average_year(year)]
