from odoo import models, fields, api, exceptions


class ReportGoal(models.AbstractModel):
    _name = 'report.bi_finance.report_ca_template'

    @api.model
    def _get_report_values(self, docids, data=None):
        yearly_goal = self.env['bi_finance.yearly_goal'].browse(docids)
        months = self._get_months(docids)
        months_ids = self._get_month_ids(months)

        employees = self._get_employees(months_ids)
        employees_ids = self._get_employees_ids(employees)

        real_annual_sales = self._cumulative_data(self._compute_annual_sales(yearly_goal.year))
        goal_annual_sales = self._cumulative_data(self._compute_goal_annual_sales(yearly_goal.year))

        report_obj = self.env['ir.actions.report']
        report = report_obj._get_report_from_name('bi_finance.report_ca_template')

        docargs = {
            'year': yearly_goal.year,
            'real_annual_sales': real_annual_sales,
            'goal_annual_sales': goal_annual_sales,
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

    def _get_sale_oders(self,year_goal,month_goal):
        request =("select SUM(s.amount_untaxed), TO_CHAR(s.date_order, 'YYYY') AS Year, "+
                  "TO_CHAR(s.date_order, 'MM') AS Month "+
                  "From sale_order s "+
                  "WHERE TO_CHAR(s.date_order, 'YYYY MM') = '"+year_goal+" "+month_goal+"'"
                  "AND s.state = 'sale' "
                  "GROUP BY Year,Month ")
        self.env.cr.execute(request)
        return self.env.cr.fetchall()

    def _compute_annual_sales(self,year):
        real_annual_sales = []
        for i in range(1,13):
            real_annual_sales.append(self._get_sale_oders(year,"{:02d}".format(i)))
        return real_annual_sales

    def _compute_goal_annual_sales(self,year):
        goal_annual_sales = []
        for i in range(1,13):
            goal_annual_sales.append(self._get_goal_sale_oders(year,str(i)))
        return goal_annual_sales

    def _get_goal_sale_oders(self, year,month):
        request = ("select SUM(e.goal), y.year AS Year, m.month AS Month " +
                   "From bi_finance_monthly_goal_employee e " +
                   "JOIN bi_finance_monthly_goal m on m.id = e.monthly_goal_id " +
                   "JOIN bi_finance_yearly_goal y on y.id = m.yearly_goal_id " +
                   "WHERE y.year = '" + year + "' AND m.month = '" + month + "' "+
                   "GROUP BY Year,Month")
        self.env.cr.execute(request)
        return self.env.cr.fetchall()

    def _cumulative_data(self,list):
        new_list = []
        cumulative_data = 0
        for r in list:
            if len(r) != 0 :
                cumulative_data += r[0][0]
                new_list.append(cumulative_data)
            else:
                new_list.append('null')
        return new_list
