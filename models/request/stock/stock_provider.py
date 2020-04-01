from ....models.request.stock.stock_treatment import StockTreatment
from ....models.request.sale_order.sale_order_treatment import SaleOrderTreatment
from ....classes.date_delivery import DateDelivery
from ....classes.color_picker import ColorPicker

class StockProvider:
    MONTHS = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12]
    def __init__(self, year, id_company, odoo):
        self._year = year
        self._factory = StockTreatment(year, id_company, odoo)
        self._ca_factory = SaleOrderTreatment(year,odoo,"","all")

    def stock(self):
        goal= self._factory.get_goal()
        result = self._factory.get_result()
        result = self.null_value_futur(result)

        return [self.MONTHS,result,goal]

    def stock_cat(self):
        color = ColorPicker()
        cats = self._ca_factory.get_all_cat()
        all_stock = []
        i = 0
        for cat in cats:
            goal= self._factory.get_goal(cat[0])
            result = self._factory.get_result(cat[0])
            result = self.null_value_futur(result)
            all_stock.append([cat[1],color.colors_dark(i),result,color.colors(i),goal])
            i +=1

        return [self.MONTHS,all_stock]

    def null_value_futur(self,list):
        return DateDelivery(list, self._year).new_list
