from odoo import models, fields, api, exceptions

class BrandGoal(models.Model):
    _name = 'bi_finance.brand_goal_stock'
    _description = 'Objectif de stock sur marque'


    brand_id = fields.Many2one('bi_finance.brand',
                                     ondelete='cascade', string="Marque", default=1, required=True)

    monthly_goal_id = fields.Many2one('bi_finance.monthly_goal',
                                     ondelete='cascade')
    currency_id = fields.Many2one(
        'res.currency', string='Currency')

    goal = fields.Monetary(string="Objectif", required=True)