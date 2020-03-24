class EbitdaSql:
    def __init__(self,id_company,year,id_goal,odoo):
        self._id_company = id_company
        self._id_goal = id_goal
        self._year = year
        self._month = 0
        self._odoo = odoo

    def set_month(self, month):
        self._month = month

    def get_goal(self):
        request = ("select m.goal_ebitda " +
                   "From bi_finance_monthly_goal m " +
                   "JOIN bi_finance_yearly_goal y on y.id = m.yearly_goal_id " +
                   "WHERE y.year = '" + str(self._year) + "' " +
                   "AND m.month = '" + str(self._month) + "' " +
                   "AND y.company_id = '"+ str(self._id_company)+"' " +
                   "AND y.id = '"+ str(self._id_goal)+"'")
        self._odoo.env.cr.execute(request)
        return self._odoo.env.cr.fetchall()

