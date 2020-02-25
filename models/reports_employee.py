from odoo import models, api

from ..classes.average import AverageList, Average


class ReportGoalEmployee(models.AbstractModel):
    _name = 'report.bi_finance.report_ca_employee_template'

    @api.model
    def _get_report_values(self, docids, data=None):
        yearly_goal = self.env['bi_finance.yearly_goal'].browse(docids)
        currency_id = self.env.ref('base.main_company').currency_id

        #employee_goal
            #normal
        context = self._context
        current_uid = context.get('uid')
        name_user = self._get_name_user(current_uid)

        employe_goal_annual_sales = self._compute_goal(yearly_goal.year,current_uid)
        employe_annual_sales = self._compute_annual_sales(yearly_goal.year,current_uid)
        employe_average_real_goal = AverageList(employe_annual_sales).compute_average(yearly_goal.year,employe_goal_annual_sales)
        sum_employe_annual_sales = self._compute_sum_data(employe_goal_annual_sales,employe_annual_sales,yearly_goal.year)

            #cumulative
        cumulative_employe_goal_annual_sales = AverageList(employe_goal_annual_sales).cumulative_data_1d(False)
        cumulative_employe_annual_sales = AverageList(employe_annual_sales).cumulative_data_1d(True)
        cumulative_employe_average_real_goal = AverageList(cumulative_employe_annual_sales).compute_average(yearly_goal.year,cumulative_employe_goal_annual_sales)
        cumulative_sum_employe_annual_sales = sum_employe_annual_sales


        docargs = {
            'year': yearly_goal.year,
            'name_user': name_user,
            'currency_id': currency_id,
            'zero_value': 0,
            'employe_annual_sales': employe_annual_sales,
            'employe_goal_annual_sales': employe_goal_annual_sales,
            'employe_average_real_goal': employe_average_real_goal,
            'sum_employe_annual_sales': sum_employe_annual_sales,
            'cumulative_employe_goal_annual_sales': cumulative_employe_goal_annual_sales,
            'cumulative_employe_annual_sales': cumulative_employe_annual_sales,
            'cumulative_employe_average_real_goal': cumulative_employe_average_real_goal,
            'cumulative_sum_employe_annual_sales': cumulative_sum_employe_annual_sales,
            'doc_model': 'bi_finance.yearly_goal'
        }
        return docargs

    def _get_sale_oders(self, year_goal, month_goal,user_id):
        request = ("select SUM(s.amount_untaxed), TO_CHAR(s.date_order, 'YYYY') AS Year, " +
                   "TO_CHAR(s.date_order, 'MM') AS Month " +
                   "From sale_order s " +
                   "WHERE TO_CHAR(s.date_order, 'YYYY MM') = '" + year_goal + " " + month_goal + "'"
                    "AND s.state = 'sale' "
                    "And s.user_id = '"+str(user_id)+"'"
                    "GROUP BY Year,Month ")
        self.env.cr.execute(request)
        return self.env.cr.fetchall()

    def _compute_annual_sales(self, year,user):
        employee_goal = []
        for i in range(1, 13):
            goal = self._get_sale_oders(year, "{:02d}".format(i),user)
            if len(goal) != 0:
                employee_goal.append(goal[0][0])
            else:
                employee_goal.append(0)
        return employee_goal

    def _compute_goal(self, year,user):
        employee_goal = []
        for i in range(1, 13):
            goal = self._get_goal_of_user(user,year, str(i))
            if len(goal) != 0:
                employee_goal.append(goal[0][0])
            else:
                employee_goal.append(0)
        return employee_goal

    def _get_goal_of_user(self, user, year, month):
        request = ("select SUM(e.goal), y.year AS Year, m.month AS Month " +
                   "From bi_finance_monthly_goal_employee e " +
                   "JOIN bi_finance_monthly_goal m on m.id = e.monthly_goal_id " +
                   "JOIN bi_finance_yearly_goal y on y.id = m.yearly_goal_id " +
                   "JOIN res_users u on u.id = e.commercial_id " +
                   "JOIN res_partner p on p.id = u.partner_id " +
                   "WHERE y.year = '" + str(year) + "' AND m.month = '" + str(month) + "' AND u.id = '" + str(user) + "' " +
                   "GROUP BY Year,Month,p.name ")
        self.env.cr.execute(request)
        return self.env.cr.fetchall()

    def _compute_sum_data(self,employe_goal_annual_sales,employe_annual_sales,year):
        sum_employe_goal = AverageList(employe_goal_annual_sales).sum_data_1d()
        sum_employe_real = AverageList(employe_annual_sales).sum_data_1d()
        sum_employe_average = Average(sum_employe_real,sum_employe_goal).get_pourcentage_formated()
        sum_employe_average_in_time = Average(sum_employe_real,sum_employe_goal).compute_in_time_average_year(year)
        sum_employe_annual_sales = [sum_employe_real,sum_employe_goal,sum_employe_average,sum_employe_average_in_time]
        return sum_employe_annual_sales

    def _get_name_user(self, user_id):
        request = ("select p.name " +
                   "From res_users u " +
                   "JOIN res_partner p on u.partner_id = p.id " +
                   "WHERE u.id = '"+str(user_id)+"' " )
        self.env.cr.execute(request)
        return self.env.cr.fetchone()[0]