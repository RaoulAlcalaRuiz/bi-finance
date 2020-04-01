from odoo import models, fields, api, exceptions

class ProductCategory(models.Model):
    _inherit = 'product.category'

    id_brand = fields.Many2one('bi_finance.brand',
                                     ondelete='set null', string="Marque")
