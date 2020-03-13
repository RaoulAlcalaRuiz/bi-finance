
def get_sale_oders(self, year_goal, month_goal):
    request = ("select SUM(s.amount_untaxed), TO_CHAR(s.commitment_date, 'YYYY') AS Year, " +
               "TO_CHAR(s.commitment_date, 'MM') AS Month " +
               "From sale_order s " +
                "Join account_move a on a.invoice_origin = s.name "+
               "WHERE TO_CHAR(s.commitment_date, 'YYYY MM') = '" + year_goal + " " + month_goal + "' "+
                "AND s.state = 'sale' "+
                "And a.state = 'posted' "+
                "GROUP BY Year,Month ")
    self.env.cr.execute(request)
    return self.env.cr.fetchall()

def get_sale_oders_user(self, year_goal, month_goal,user_id):
    request = ("select s.amount_untaxed, TO_CHAR(s.commitment_date, 'YYYY') AS Year, "+
                "TO_CHAR(s.commitment_date, 'MM') AS Month "+
                "From sale_order s "+
                "join account_move a on a.invoice_origin = s.name "+
                "WHERE TO_CHAR(s.commitment_date, 'YYYY MM') = '" + year_goal + " " + month_goal + "'"+
                "AND s.state = 'sale' "+
                "And a.state = 'posted' "+
                "And s.user_id = '"+str(user_id)+"'")

    self.env.cr.execute(request)
    return self.env.cr.fetchall()