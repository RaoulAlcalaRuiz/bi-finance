from odoo import models, fields, api, exceptions

class ProductCatCa(models.Model):
    _name = 'bi_finance.product_cat_ca'
    _description = 'Objectif sur catégorie'


    cat_product_id = fields.Many2one('product.category',
                                     ondelete='cascade', string="Catégorie", default=1, required=True)

    monthly_goal_employee_id = fields.Many2one('bi_finance.monthly_goal_employee',
                                     ondelete='cascade')
    currency_id = fields.Many2one(
        'res.currency', string='Currency')

    goal = fields.Monetary(string="Objectif", required=True)