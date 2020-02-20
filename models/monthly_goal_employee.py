from odoo import models, fields, api, exceptions


class monthlyGoalEmployee(models.Model):
     _name = 'bi_finance.monthly_goal_employee'

     name = fields.Char(string="Titre", compute='_compute_name')
     currency_id = fields.Many2one(
          'res.currency', string='Currency')
     goal = fields.Monetary(string="Objectif", required=True, help="Objectif du chiffre d'affaire du mois pour le commercial")

     monthly_goal_id = fields.Many2one('bi_finance.monthly_goal',
          ondelete='cascade', string="Objectif mensuel", required=True)

     commercial_id = fields.Many2one('res.users',
        ondelete='set null', string="Commercial", index=True)

     @api.onchange('commercial_id',' monthly_goal_id')
     def _compute_name(self):
          for record in self:
               if not record.monthly_goal_id and not record.commercial_id:
                    record.name = "nom mois {annee}".format(
                         annee=record.monthly_goal_id.yearly_goal_id.year)

               elif not record.monthly_goal_id :
                    record.name = "{nom} mois {annee}".format(
                         nom = record.commercial_id.name,
                         annee=record.monthly_goal_id.yearly_goal_id.year)

               elif not record.commercial_id :
                    record.name = "commercial mois {annee}".format(
                         annee=record.monthly_goal_id.yearly_goal_id.year)
               else :
                    record.name = "{nom} {mois} {annee}".format(
                         nom = record.commercial_id.name,
                         mois=record.monthly_goal_id.month,
                         annee=record.monthly_goal_id.yearly_goal_id.year)