def get_sale_oders_ind_sql(self, str_ids):
    request = ("select s.user_id, SUM(s.amount_untaxed)"+
                "From sale_order s "+
                "WHERE s.commitment_date IS NULL "+
                "AND s.state = 'sale' "+
                "And s.user_id in ("+str_ids+") "+
                "group by s.user_id")
    self.env.cr.execute(request)
    return self.env.cr.fetchall()