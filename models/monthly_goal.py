from odoo import models, fields, api, exceptions


class monthlyGoal(models.Model):
    _name = 'bi_finance.monthly_goal'
    _description = 'Objectif Mensuel'

    name = fields.Char(string="Titre", compute='_compute_name')
    month = fields.Selection(selection='_month', string='Mois', required=True)

    goal_percentage_in_time = fields.Percent(string="Pourcentage",required=True,help="Objectif du nombre de livraison livrée à temps (en %)", default=0)
    day_before_delivery = fields.Integer(string="Delai d'avance",required=True,help="Delai d'avance sur la livraison (jour)", default=5)
    quality = fields.Percent(string="Qualité",required=True,help="Objectif du nombre des produits livrés sans problème de qualité (en %)", default=0)

    currency_id = fields.Many2one(
        'res.currency', string='Currency')
    goal = fields.Monetary(string="Objectif du mois", compute='_goal_compute')
    stock = fields.Monetary(string="Stock")
    goal_ebitda = fields.Monetary(string="Ebitda")

    yearly_goal_id = fields.Many2one('bi_finance.yearly_goal',
                                     ondelete='cascade', string="Objectif annuel", required=True)

    monthly_goal_employee_ids = fields.One2many(
        'bi_finance.monthly_goal_employee', 'monthly_goal_id', string="Objectif mensuels des employés")

    @api.depends('goal', 'monthly_goal_employee_ids')
    def _goal_compute(self):
        for r in self:
            if 0 == len(r.monthly_goal_employee_ids):
                r.goal = 0
            else:
                for m in r.monthly_goal_employee_ids:
                    r.goal += m.goal

    @api.onchange('month', ' yearly_goal_id')
    def _compute_name(self):
        for record in self:
            if record.month == '' and not record.yearly_goal_id:
                record.name = "mois annee"

            elif not record.yearly_goal_id:
                record.name = "{mois} année".format(mois=self._month()[int(record.month) - 1][1])

            elif record.month == '':
                record.name = "mois {annee}".format(annee=record.yearly_goal_id.year)
            else:
                record.name = "{mois} {annee}".format(mois=self._month()[int(record.month) - 1][1],
                                                      annee=record.yearly_goal_id.year)

    def _month(self):
        list_month = [('1', 'Janvier'), ('2', 'Février'), ('3', 'Mars')
            , ('4', 'Avril'), ('5', 'Mai'), ('6', 'Juin')
            , ('7', 'Juillet'), ('8', 'Aout'), ('9', 'Septembre')
            , ('10', 'Octobre'), ('11', 'Novembre'), ('12', 'Décembre')]
        return list_month
