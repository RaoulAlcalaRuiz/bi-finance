from ....classes.treatment_factory import TreatmentFactory
from ....classes.result_interpretation import ResultInterpretationZero
from ....models.request.sale_order.sale_order_sql import SaleOrderSql


class SaleOrderTreatment :
    def __init__(self,year,odoo,treatment,user_id):
        self._year = year
        self._interpretation = ResultInterpretationZero()
        self._user_id = user_id
        self._sql = SaleOrderSql(year, odoo)
        self._treatment = TreatmentFactory(treatment).get_treatment()

    # Annual request
    def annual_sales(self):
        annual_sales = []
        for i in range(1, 13):
            month_result = self.month_sales(i)
            annual_sales.append(month_result)
        treatment = self._treatment.treatment(annual_sales, "real")
        total = self._treatment.sum(treatment)

        return [treatment,total]

    def annual_sales_goal(self):
        annual_sales_goal = []
        for i in range(1, 13):
            month_result = self.month_sales_goal(i)
            annual_sales_goal.append(month_result)
        treatment = self._treatment.treatment(annual_sales_goal, "goal")
        total = self._treatment.sum(annual_sales_goal)

        return [treatment,total]

    def annual_forecast(self):
        annual_forecast = []
        for i in range(1, 13):
            month_result = self.month_forecast(i)
            annual_forecast.append(month_result)

        treatment = self._treatment.treatment(annual_forecast, "real")
        total = self._treatment.sum(treatment)

        return [treatment,total]

    # Ne fonctionne que avec une id reçus
    def date_ind(self):
        date_ind = self._sql.get_sale_oders_ind_sql(self._user_id)
        name = ""
        ind = 0
        if len(date_ind) != 0 :
            name = self._sql.get_name_employee(date_ind[0])[0]
            ind = date_ind[1]
        else:
            name = self._sql.get_name_employee(self._user_id)[0]
        return [(name, ind)]

    def annual_sales_goal_employee(self):
        ids = self.get_ids_employee()
        goals = []
        for id in ids:
            self._user_id = id[0]
            goal = self.annual_sales_goal()
            goals.append((id[1],goal[0],goal[1]))
        return goals

    def get_ids_employee(self):
        if self._user_id == "all":
            ids = self._sql.get_user_id_have_goal()
        else:
            ids = [(self._user_id, self._sql.get_name_employee(self._user_id))]

        return ids



    # Month request
    def month_sales_goal(self, month):
        self.change_month(month)
        result_sql = self._sql.get_goal_sale_oders(self._user_id)
        return self.interpretation(result_sql)

    def month_sales(self, month):
        self.change_month(self.format_month(month))
        result_sql = self._sql.get_sale_oders(self._user_id)
        return self.interpretation(result_sql)

    def month_forecast(self, month):
        self.change_month(self.format_month(month))
        result_sql = self._sql.get_sale_oders_forecast(self._user_id)
        return self.interpretation(result_sql)


    # Générique
    def interpretation(self,result):
        return self._interpretation.interpretation(result)

    def change_month(self,month):
        self._sql.set_month(month)

    def format_month(self,month):
        return "{:02d}".format(month)

