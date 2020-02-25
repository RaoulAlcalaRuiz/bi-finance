from odoo import fields, models

class Partner(models.Model):
    _inherit = 'res.user'

    # Add a new column to the res.partner model, by default partners are not
    # instructors
    commercial = fields.Boolean("Commercial", default=False)
