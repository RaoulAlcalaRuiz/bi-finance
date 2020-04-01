from ..request.stock.stock_provider import StockProvider

from odoo import models, api

class ReportStock(models.AbstractModel):
    _name = 'report.bi_finance.stock_report_template'

    @api.model
    def _get_report_values(self, docids, data=None):
        yearly_goal = self.env['bi_finance.yearly_goal'].browse(docids)
        currency_id = self.env.ref('base.main_company').currency_id
        year = yearly_goal.year
        id_company = self._get_id_company(docids)

        provider = StockProvider(year, id_company, self)
        stock = provider.stock()

        stock_cat = provider.stock_cat()
        docargs = {
            'stock': stock,
            'stock_cat': stock_cat,
            'year': year,
            'currency_id': currency_id,
            'zero_value': 0,
            'doc_model': 'bi_finance.yearly_goal'
        }
        return docargs

    def _get_id_company(self, id):
        return self.env['bi_finance.yearly_goal'].search([("id", "in", id)])[0].company_id.id