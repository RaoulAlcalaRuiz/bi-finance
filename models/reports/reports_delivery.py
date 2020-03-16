from odoo import models, api

from ..request.customer.customer_satisfaction_provider import CustomerSatisfactionProvider


class ReportGoalEmployee(models.AbstractModel):
    _name = 'report.bi_finance.delivery_in_time_report_template'

    @api.model
    def _get_report_values(self, docids, data=None):
        yearly_goal = self._get_current_year(docids)
        year = yearly_goal.year
        currency_id = self.env.ref('base.main_company').currency_id
        id_company = self._get_id_company(docids)
        id_goal = docids[0]

        provider = CustomerSatisfactionProvider(id_company,year,id_goal,self)
        result = provider.delivery_in_time()
        delivery_in_time = result[0]
        delivery_in_time_formated = result[1]

        result = provider.quality()
        quality_delivery = result[0]
        quality_delivery_formated = result[1]

        docargs = {
            'year': year,
            'currency_id': currency_id,
            'zero_value': 0,
            'doc_model': 'bi_finance.yearly_goal',
            'delivery_in_time': delivery_in_time,
            'delivery_in_time_formated': delivery_in_time_formated,
            'quality_delivery': quality_delivery,
            'quality_delivery_formated': quality_delivery_formated
        }
        return docargs

    def _get_current_year(self, id):
        return self.env['bi_finance.yearly_goal'].browse(id)

    def _get_id_company(self, id):
        return self.env['bi_finance.yearly_goal'].search([("id", "in", id)])[0].company_id.id