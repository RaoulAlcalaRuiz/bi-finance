from ....models.request.stock.stock_treatment import StockTreatment
from ....classes.date_delivery import DateDelivery

class StockProvider:
    MONTHS = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12]
    def __init__(self, year, id_company, odoo):
        self._year = year
        self._factory = StockTreatment(year, id_company, odoo)

    def stock(self):
        goal= self._factory.get_goal()
        result = self._factory.get_result()
        result = self.null_value_futur(result)

        return [self.MONTHS,result,goal];

    def null_value_futur(self,list):
        return DateDelivery(list, self._year).new_list
