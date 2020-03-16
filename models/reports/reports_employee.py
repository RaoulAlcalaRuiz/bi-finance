from odoo import models, api

from ..request.sale_order.sale_order_provider import SaleOrderProvider
from ...models.sql_request import _get_name_user


class ReportGoalEmployee(models.AbstractModel):
    _name = 'report.bi_finance.report_ca_employee_template'

    @api.model
    def _get_report_values(self, docids, data=None):
        yearly_goal = self.env['bi_finance.yearly_goal'].browse(docids)
        currency_id = self.env.ref('base.main_company').currency_id
        year = yearly_goal.year

        #current id
        context = self._context
        current_uid = context.get('uid')
        name_user = _get_name_user(self,current_uid)

        provider = SaleOrderProvider(year,self,"cumulative",current_uid)
        annual_sales_cumulative = provider.annual_sales()

        provider = SaleOrderProvider(year,self,"normal",current_uid)
        annual_sales = provider.annual_sales()

        annual_forecast = provider.annual_forecast()
        date_ind = provider.date_ind()

        docargs = {
            'year': yearly_goal.year,
            'name_user': name_user,
            'currency_id': currency_id,
            'zero_value': 0,
            'doc_model': 'bi_finance.yearly_goal',
            'annual_sales': annual_sales,
            'annual_sales_cumulative': annual_sales_cumulative,
            'annual_forecast': annual_forecast,
            'date_ind': date_ind,
        }
        return docargs
