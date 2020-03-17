from ....classes.management_list import ManagementList
from ....classes.average import Average
from ....classes.average_list import AverageList
from ....models.request.sale_order.sale_order_treatment import SaleOrderTreatment

class SaleOrderProvider:
    MONTHS = [1,2,3,4,5,6,7,8,9,10,11,12]

    def __init__(self, year, odoo, treatment, user_id):
        self._year = year
        self._factory = SaleOrderTreatment(year,odoo,treatment, user_id)

    # [months,Resultats,Objectifs,[réaliser, indicateur],[total_resultat,total_objectif,[total_réaliser, indicateur]]]
    def annual_sales(self):
        sales = self._factory.annual_sales()
        goal = self._factory.annual_sales_goal()
        average = self.average(sales[0],goal[0])
        return [self.MONTHS,
                sales[0],
                goal[0],
                average,
                [sales[1],goal[1],self.average_year(sales[1],goal[1])]]

    def annual_goal_employee(self):
        return self._factory.annual_sales_goal_employee()

    def annual_forecast(self):
        sales = self._factory.annual_sales()
        goal = self._factory.annual_sales_goal()
        forecast = self._factory.annual_forecast()
        percentage = self.average(sales[0],forecast[0])
        difference = ManagementList(forecast[0]).compute_difference(sales[0])
        total_forecast_average = self.average_year(sales[1],forecast[1])
        total_difference = forecast[1] - sales[1]
        return [self.MONTHS,
                goal[0],
                sales[0],
                forecast[0],
                percentage,
                difference,
                [goal[1],sales[1],forecast[1],total_forecast_average,total_difference]
                ]

    def date_ind(self):
        return self._factory.date_ind()

    def average(self,real,goal):
        return AverageList(real,goal).compute_average(self._year)

    def average_year(self,real,goal):
        av = Average(real, goal)
        return [av.get_pourcentage_formated(),av.compute_in_time_average_year(self._year)]