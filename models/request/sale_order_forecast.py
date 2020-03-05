def get_sale_oders_forecast(self, year_goal, month_goal,user_id):
    request = ("select SUM(s.amount_untaxed), TO_CHAR(s.commitment_date, 'YYYY') AS Year, " +
               "TO_CHAR(s.commitment_date, 'MM') AS Month " +
               "From sale_order s " +
               "WHERE TO_CHAR(s.commitment_date, 'YYYY MM') = '" + year_goal + " " + month_goal + "'"
                "AND s.state = 'sale' "
                "And s.user_id = '"+str(user_id)+"'"
                "GROUP BY Year,Month ")
    self.env.cr.execute(request)
    return self.env.cr.fetchall()