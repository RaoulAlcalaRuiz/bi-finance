from odoo import models, fields, api, exceptions
from datetime import datetime

class yearlyGoal(models.Model):
    _name = 'bi_finance.yearly_goal'
    _description = 'Objectif Annuel'

    name = fields.Char(string="Titre", compute='_compute_name')
    year = fields.Selection(selection='_years', string='Année', required=True)

    description = fields.Text(string="Description", help="Descrivez les objectifs de cette annnée.")

    currency_id = fields.Many2one(
        'res.currency', string='Currency')
    goal = fields.Monetary(string="Objectif de l'année", help='Ce champ sera calculé grace aux objectifs mensuels',
                           compute='_goal_compute_year')

    company_id = fields.Many2one('res.company',
                                     ondelete='cascade', string="Société", default=1, required=True)

    monthly_goal_ids = fields.One2many(
        'bi_finance.monthly_goal', 'yearly_goal_id', string="Objectif mensuels")

    _sql_constraints = [
        ('year_unique',
         'UNIQUE(year)',
         "Vous ne pouvez pas créer plusieurs objectifs la même année")
    ]

    @api.depends('goal', 'monthly_goal_ids')
    def _goal_compute_year(self):
        for r in self:
            goal = 0
            if (0 != len(r.monthly_goal_ids)):
                for monthly_record in r.monthly_goal_ids:
                    if (0 != len(monthly_record.monthly_goal_employee_ids)):
                        for employee in monthly_record.monthly_goal_employee_ids:
                            goal += employee.goal
            r.goal = goal

    def _current_year(self):
        return str(datetime.today().year)

    def _years(self):
        list_years = []
        current_year = self._current_year()
        before_year = int(current_year) - 10
        later_year = int(current_year) + 20
        for i in range(before_year, later_year):
            list_years.append((str(i), str(i)))
        return list_years

    @api.onchange('year')
    def _compute_name(self):
        for record in self:
            record.name = record.year

    def _get_all_employee(self):
        list_commercial = []
        for r in self:
            if 0 == len(r.monthly_goal_ids):
                return list_commercial
            else:
                for monthly_record in r.monthly_goal_ids:
                    if 0 != len(monthly_record.monthly_goal_employee_ids):
                        for employee in monthly_record.monthly_goal_employee_ids:
                            list_commercial.append(employee.commercial_id.user_id)
        return list_commercial

