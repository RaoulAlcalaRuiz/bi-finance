from odoo import models, fields, api, exceptions

class Brand(models.Model):
    _name = 'bi_finance.brand'
    _description = 'Permet d\'associer une marque à des catégories'
    _rec_name = 'name_brand'

    name_brand = fields.Char(string="Nom de la marque",required=True)

    cat_product_ids = fields.One2many(
        'product.category', 'id_brand', string="Catégories d'articles")