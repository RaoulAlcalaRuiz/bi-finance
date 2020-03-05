from odoo import models, api

from .request.sale_order import get_sale_oders
from .request.sale_order_goal import get_user_id_have_goal, get_goal_of_user, get_goal_sale_oders
from ..classes.average import AverageList, Average


class ReportGoal(models.AbstractModel):
    _name = 'report.bi_finance.report_ca_template'

    @api.model
    def _get_report_values(self, docids, data=None):
        yearly_goal = self.env['bi_finance.yearly_goal'].browse(docids)
        currency_id = self.env.ref('base.main_company').currency_id

        real_annual_sales_draft = self._compute_annual_sales(yearly_goal.year)
        goal_annual_sales_draft = self._compute_goal_annual_sales(yearly_goal.year)

        # Cumulative data
        real_annual_sales = AverageList(real_annual_sales_draft).cumulative_data(True)
        goal_annual_sales = AverageList(goal_annual_sales_draft).cumulative_data(False)

        average_real_goal = AverageList(real_annual_sales).compute_average(yearly_goal.year, goal_annual_sales)

        sum_annual_sales = [AverageList(real_annual_sales_draft).sum_data(),
                            AverageList(goal_annual_sales_draft).sum_data()]

        sum_annual_sales.append(
            Average(sum_annual_sales[0], sum_annual_sales[1]).get_pourcentage_formated()
        )
        sum_annual_sales.append(
            Average(sum_annual_sales[0], sum_annual_sales[1]).compute_in_time_average_year(yearly_goal.year))

        # Normal Data
        normal_real_annual_sales = AverageList(real_annual_sales_draft).extract_first_value()
        normal_goal_annual_sales = AverageList(goal_annual_sales_draft).extract_first_value()

        normal_average_real_goal = AverageList(normal_real_annual_sales).compute_average(yearly_goal.year,
                                                                                         normal_goal_annual_sales)

        #employee_id
        employe_annual_sales = self._compute_goal_employee(yearly_goal.year)

        docargs = {
            'year': yearly_goal.year,
            'real_annual_sales': real_annual_sales,
            'goal_annual_sales': goal_annual_sales,
            'average_real_goal': average_real_goal,
            'normal_real_annual_sales': normal_real_annual_sales,
            'normal_goal_annual_sales': normal_goal_annual_sales,
            'normal_average_real_goal': normal_average_real_goal,
            'sum_annual_sales': sum_annual_sales,
            'currency_id': currency_id,
            'zero_value': 0,
            'employe_annual_sales': employe_annual_sales,
            'doc_model': 'bi_finance.yearly_goal'
        }
        return docargs

    def _compute_annual_sales(self, year):
        real_annual_sales = []
        for i in range(1, 13):
            real_annual_sales.append(get_sale_oders(self,year, "{:02d}".format(i)))
        return real_annual_sales

    def _compute_goal_annual_sales(self, year):
        goal_annual_sales = []
        for i in range(1, 13):
            goal_annual_sales.append(get_goal_sale_oders(self,year, str(i)))
        return goal_annual_sales

    def _compute_goal_employee(self, year):
        all_employee_goal = []
        employee_ids = get_user_id_have_goal(self,year)
        for id in employee_ids:
            employee_goal = []
            for i in range(1, 13):
                goal = 0
                goal = get_goal_of_user(self,id[0],year, str(i))
                if len(goal) != 0:
                    employee_goal.append(goal[0][0])
                else:
                    employee_goal.append(0)
            all_employee_goal.append((id[1],employee_goal))
        return all_employee_goal


