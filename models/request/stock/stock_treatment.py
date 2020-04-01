from ....models.request.stock.stock_sql import StockSql
from ....classes.result_interpretation import ResultInterpretationZero

class StockTreatment:
    def __init__(self,year, company_id, odoo):
        self._sql = StockSql(year, company_id, odoo)
        self._interpretation = ResultInterpretationZero()

    def get_goal(self,cat = None):
        annual_goal = []
        for i in range(1, 13):
            month_result = self.month_stock_goal(i,cat)
            annual_goal.append(month_result)
        return annual_goal

    def get_result(self,cat = None):
        annual_goal = []
        for i in range(1, 13):
            month_result = self.month_stock_result(i,cat)
            annual_goal.append(month_result)
        return annual_goal

    # Month request
    def month_stock_goal(self, month,cat):
        self.change_month(month)
        result_sql = self._sql.get_goal_stock_value(cat)
        return self.interpretation(result_sql)

    def month_stock_result(self, month,cat):
        self.change_month(month)
        result_sql = self._sql.get_stock_value(cat)
        if len(result_sql) != 0:
            return self.sum_stock_value(result_sql)
        else:
            return 0

    def sum_stock_value(self,list):
        value = 0
        for stock_value in list:
            value = stock_value[0] + value
        return value

    # Générique
    def interpretation(self,result):
        return self._interpretation.interpretation(result)

    def change_month(self, month):
        self._sql.set_month(month)