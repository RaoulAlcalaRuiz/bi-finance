from odoo import models, api

from ..request.sale_order.sale_order_provider import SaleOrderProvider


class ReportGoal(models.AbstractModel):
    _name = 'report.bi_finance.report_ca_template'

    @api.model
    def _get_report_values(self, docids, data=None):
        yearly_goal = self.env['bi_finance.yearly_goal'].browse(docids)
        currency_id = self.env.ref('base.main_company').currency_id
        year = yearly_goal.year

        provider = SaleOrderProvider(year,self,"cumulative","all")
        annual_sales_cumulative = provider.annual_sales()

        provider = SaleOrderProvider(year,self,"normal","all")
        annual_sales = provider.annual_sales()

        employe_annual_sales = provider.annual_goal_employee()
        docargs = {
            'annual_sales': annual_sales,
            'annual_sales_cumulative': annual_sales_cumulative,
            'employe_annual_sales': employe_annual_sales,
            'year': year,
            'currency_id': currency_id,
            'zero_value': 0,
            'doc_model': 'bi_finance.yearly_goal'
        }
        return docargs