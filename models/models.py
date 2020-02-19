# -*- coding: utf-8 -*-

from odoo import models, fields, api, exceptions
from datetime import datetime


class yearlyGoal(models.Model):
     _name = 'bi_finance.yearly_goal'
     _description = 'Objectif Annuel'

     name = fields.Char(string="Titre", compute='_compute_name')
     year = fields.Selection(selection='_years',string='Année', required=True)

     description = fields.Text(string="Description",help="Descrivez les objectifs de cette annnée.")

     currency_id = fields.Many2one(
          'res.currency', string='Currency')
     goal = fields.Monetary(string="Objectif de l'année", help='Ce champ sera calculé grace aux objectifs mensuel',compute='_goal_compute_year')

     monthly_goal_ids = fields.One2many(
          'bi_finance.monthly_goal', 'yearly_goal_id', string="Objectif mensuels")

     @api.depends('goal', 'monthly_goal_ids')
     def _goal_compute_year(self):
          for r in self:
                goal = 0
                if(0 != len(r.monthly_goal_ids)):
                    for monthly_record in r.monthly_goal_ids:
                         if(0 != len(monthly_record.monthly_goal_employee_ids)):
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
          for i in range(before_year,later_year):
            list_years.append((str(i),str(i)))
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
               else :
                    for monthly_record in r.monthly_goal_ids:
                         if 0 != len(monthly_record.monthly_goal_employee_ids):
                              for employee in monthly_record.monthly_goal_employee_ids :
                                   list_commercial.append(employee.commercial_id.user_id)
          return list_commercial

class monthlyGoal(models.Model):
     _name = 'bi_finance.monthly_goal'
     _description = 'Objectif Mensuel'

     name = fields.Char(string="Titre", compute='_compute_name')
     month = fields.Selection(selection='_month',string='Mois', required=True)

     currency_id = fields.Many2one(
          'res.currency', string='Currency')
     goal = fields.Monetary(string="Objectif du mois", compute='_goal_compute')

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



     @api.onchange('month',' yearly_goal_id')
     def _compute_name(self):
          for record in self:
               if record.month == '' and not record.yearly_goal_id:
                    record.name = "mois annee"

               elif not record.yearly_goal_id :
                    record.name = "{mois} année".format(mois=self._month()[int(record.month) - 1][1])

               elif record.month == '':
                    record.name = "mois {annee}".format(annee=record.yearly_goal_id.year)
               else :
                    record.name = "{mois} {annee}".format(mois=self._month()[int(record.month) - 1][1],
                                                          annee=record.yearly_goal_id.year)

     def _month(self):
          list_month = [('1','Janvier'),('2','Février'),('3','Mars')
                        ,('4','Avril'),('5','Mai'),('6','Juin')
                        ,('7','Juillet'),('8','Aout'),('9','Septembre')
                        ,('10','Octobre'),('11','Novembre'),('12','Décembre')]
          return list_month

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

class ReportGoal(models.AbstractModel):
    _name = 'report.bi_finance.report_ca_template'

    @api.model
    def _get_report_values(self, docids, data=None):
        yearly_goal = self.env['bi_finance.yearly_goal'].browse(docids)
        months = self._get_months(docids)
        months_ids = self._get_month_ids(months)

        employees = self._get_employees(months_ids)
        employees_ids = self._get_employees_ids(employees)

        sale_oders = self._get_sale_oders(employees_ids,yearly_goal.year)
        report_obj = self.env['ir.actions.report']
        report = report_obj._get_report_from_name('bi_finance.report_ca_template')

        docargs = {
            'doc_ids': docids,
            'months': months,
            'months_ids': months_ids,
            'employees': employees,
            'employees_ids': employees_ids,
            'sale_oders': sale_oders,
            'doc_model': 'bi_finance.yearly_goal'
        }
        return docargs

    def _get_months(self,yearly_goal_id):
        environementMonth = self.env['bi_finance.monthly_goal']
        return environementMonth.search([('yearly_goal_id.id','=',yearly_goal_id)])
        months_ids = self._get_id(months)

    def _get_month_ids(self,list):
        array = []
        for r in list:
            array.append(r.id)
        return array

    def _get_employees(self,months_ids):
        environementEmployee = self.env['bi_finance.monthly_goal_employee']
        return environementEmployee.search([('monthly_goal_id','=',months_ids)])

    def _get_employees_ids(self,list):
        array = []
        for r in list:
            array.append(r.commercial_id.id)
        return array

    def _get_employees_ids_str(self,employees_ids):
        string_return = "("
        index = 0
        len_id = len(employees_ids)
        for r in employees_ids:
            index += 1
            if len_id != index:
                string_return += "{id},".format(id=str(r))
            else:
                string_return += "{id}".format(id=str(r))
        string_return +=")"
        return string_return

    def _get_sale_oders(self,employees_ids,year_goal):
        request =("select s.id, s.amount_untaxed, s.date_order, s.state, s.user_id "+
                  "From sale_order s "+
                  "WHERE s.user_id in "+ self._get_employees_ids_str(employees_ids)+" "+" AND "+
                  "TO_CHAR(s.date_order,'YYYY') = '"+year_goal+"'")
        self.env.cr.execute(request)
        return self.env.cr.fetchall()