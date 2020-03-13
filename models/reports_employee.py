from odoo import models, api

from .sql_request import _get_name_user, _compute_goal, _compute_annual_sales, _compute_sum_data, \
    _compute_annual_sales_forecast, _compute_average, _get_sale_oders_ind
from ..classes.average import AverageList, Average


class ReportGoalEmployee(models.AbstractModel):
    _name = 'report.bi_finance.report_ca_employee_template'

    @api.model
    def _get_report_values(self, docids, data=None):
        yearly_goal = self.env['bi_finance.yearly_goal'].browse(docids)
        currency_id = self.env.ref('base.main_company').currency_id

        #employee_goal
        context = self._context
        current_uid = context.get('uid')
        name_user = _get_name_user(self,current_uid)

        # Résultat
            #normal
        employe_goal_annual_sales = _compute_goal(self, yearly_goal.year, current_uid)
        employe_annual_sales = _compute_annual_sales(self, yearly_goal.year, current_uid)
        employe_average_real_goal = AverageList(employe_annual_sales).compute_average(yearly_goal.year, employe_goal_annual_sales)
        sum_employe_annual_sales = _compute_sum_data(employe_goal_annual_sales, employe_annual_sales, yearly_goal.year)
            #cumulative
        cumulative_employe_goal_annual_sales = AverageList(employe_goal_annual_sales).cumulative_data_1d(False)
        cumulative_employe_annual_sales = AverageList(employe_annual_sales).cumulative_data_1d(True)
        cumulative_employe_average_real_goal = AverageList(cumulative_employe_annual_sales).compute_average(yearly_goal.year,cumulative_employe_goal_annual_sales)
        cumulative_sum_employe_annual_sales = sum_employe_annual_sales

        # Prévisions
            #normal
        employe_annual_sales_forecast = _compute_annual_sales_forecast(self,yearly_goal.year,current_uid)
        employe_average_forecast_goal = AverageList(employe_annual_sales_forecast).compute_average(yearly_goal.year,employe_goal_annual_sales)
        employe_difference_forecast_real = AverageList(employe_annual_sales_forecast).compute_difference(employe_annual_sales)
        average_sum_forecast = _compute_average(employe_annual_sales_forecast, employe_goal_annual_sales, yearly_goal.year)
        sum_employe_annual_sales_forecast = [AverageList(employe_annual_sales).sum_data_1d(),
                                    AverageList(employe_annual_sales_forecast).sum_data_1d(),
                                    AverageList(employe_goal_annual_sales).sum_data_1d(),
                                    average_sum_forecast[0],average_sum_forecast[1],
                                    AverageList(employe_difference_forecast_real).sum_data_1d()]

        # Date ind.
        date_ind = _get_sale_oders_ind(self,[current_uid])

        docargs = {
            'year': yearly_goal.year,
            'name_user': name_user,
            'currency_id': currency_id,
            'zero_value': 0,
            'employe_annual_sales': employe_annual_sales,
            'employe_goal_annual_sales': employe_goal_annual_sales,
            'employe_average_real_goal': employe_average_real_goal,
            'sum_employe_annual_sales': sum_employe_annual_sales,
            'cumulative_employe_goal_annual_sales': cumulative_employe_goal_annual_sales,
            'cumulative_employe_annual_sales': cumulative_employe_annual_sales,
            'cumulative_employe_average_real_goal': cumulative_employe_average_real_goal,
            'cumulative_sum_employe_annual_sales': cumulative_sum_employe_annual_sales,
            'employe_annual_sales_forecast': employe_annual_sales_forecast,
            'employe_average_forecast_goal': employe_average_forecast_goal,
            'employe_difference_forecast_real': employe_difference_forecast_real,
            'sum_employe_annual_sales_forecast': sum_employe_annual_sales_forecast,
            'date_ind': date_ind,
            'doc_model': 'bi_finance.yearly_goal'
        }
        return docargs