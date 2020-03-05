# récupère tout user id ayant un objectif sur le CA
def get_user_id_have_goal(self, year):
    request = ("select Distinct(u.id), p.name AS Employee " +
               "From bi_finance_monthly_goal_employee e " +
               "JOIN bi_finance_monthly_goal m on m.id = e.monthly_goal_id " +
               "JOIN bi_finance_yearly_goal y on y.id = m.yearly_goal_id " +
               "JOIN res_users u on u.id = e.commercial_id " +
               "JOIN res_partner p on p.id = u.partner_id " +
               "WHERE y.year = '" + year + "' ")
    self.env.cr.execute(request)
    return self.env.cr.fetchall()


def get_goal_of_user(self, user, year, month):
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

def get_goal_sale_oders(self, year, month):
    request = ("select SUM(e.goal), y.year AS Year, m.month AS Month " +
               "From bi_finance_monthly_goal_employee e " +
               "JOIN bi_finance_monthly_goal m on m.id = e.monthly_goal_id " +
               "JOIN bi_finance_yearly_goal y on y.id = m.yearly_goal_id " +
               "WHERE y.year = '" + year + "' AND m.month = '" + month + "' " +
               "GROUP BY Year,Month")
    self.env.cr.execute(request)
    return self.env.cr.fetchall()