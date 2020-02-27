# -*- coding: utf-8 -*-
from odoo import fields, models

class Order(models.Model):
    _inherit = 'sale.order'

    commitment_date = fields.Datetime(required=True)
