from .ebitda_sql import EbitdaSql
from ....classes.result_interpretation import ResultInterpretationZero
from ....classes.treatment_factory import TreatmentFactory

class EbitdaTreatment:
    def __init__(self,id_company,year,id_goal,odoo,treatment):
        self._sql = EbitdaSql(id_company,year,id_goal,odoo)
        self._interpretation = ResultInterpretationZero()
        self._treatment = TreatmentFactory(treatment).get_treatment()

    def get_goal(self):
        annual_sales = []
        for i in range(1, 13):
            month_result = self.month_goal(i)
            annual_sales.append(month_result)
        treatment = self._treatment.treatment(annual_sales, "goal")
        total = self._treatment.sum(treatment)

        return [treatment,total]

    def month_goal(self, month):
        self.change_month(month)
        result_sql = self._sql.get_goal()
        return self.interpretation(result_sql)

    # Générique
    def interpretation(self,result):
        return self._interpretation.interpretation(result)

    def change_month(self,month):
        self._sql.set_month(month)

    def format_month(self,month):
        return "{:02d}".format(month)
