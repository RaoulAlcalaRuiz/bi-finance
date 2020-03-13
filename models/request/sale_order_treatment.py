from ...classes.treatment_factory import TreatmentFactory
from ...classes.result_interpretation import ResultInterpretationZero
from ..request.sale_order_sql import SaleOrderSql


class SaleOrderTreatment :
    def __init__(self,year,odoo,treatment):
        self._year = year
        self._interpretation = ResultInterpretationZero()
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

    # Month request
    def month_sales_goal(self, month):
        self.change_month(month)
        result_sql = self._sql.get_goal_sale_oders()
        return self.interpretation(result_sql)

    def month_sales(self, month):
        self.change_month(self.format_month(month))
        result_sql = self._sql.get_sale_oders()
        return self.interpretation(result_sql)



    def interpretation(self,result):
        return self._interpretation.interpretation(result)

    def change_month(self,month):
        self._sql.set_month(month)

    def format_month(self,month):
        return "{:02d}".format(month)


