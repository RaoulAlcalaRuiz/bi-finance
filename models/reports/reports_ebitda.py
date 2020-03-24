from odoo import models, api

from ..request.ebitda.ebitda_provider import EbitdaProvider

class ReportStock(models.AbstractModel):
    _name = 'report.bi_finance.ebitda_report_template'

    @api.model
    def _get_report_values(self, docids, data=None):
        yearly_goal = self.env['bi_finance.yearly_goal'].browse(docids)
        currency_id = self.env.ref('base.main_company').currency_id
        year = yearly_goal.year
        id_goal = docids[0]
        id_company = self._get_id_company(docids)

        ebitba_provider = EbitdaProvider(id_company , year, id_goal, self)
        ebitda = ebitba_provider.ebitda()

        docargs = {
            'year': year,
            'currency_id': currency_id,
            'ebitda': ebitda,
            'zero_value': 0,
            'doc_model': 'bi_finance.yearly_goal'
        }
        return docargs

    def _get_id_company(self, id):
        return self.env['bi_finance.yearly_goal'].search([("id", "in", id)])[0].company_id.id