class SaleOrderSql:
    def __init__(self, year, odoo):
        self._year = str(year)
        self._month = '0'
        self._odoo = odoo

    def set_month(self, month):
        self._month = str(month)

    def get_sale_oders(self,user_id,cat):
        user_condition = ""
        cat_condition = ""
        if str(user_id) != "all":
            user_condition = "And s.user_id = '" + str(user_id) + "'"
        if cat:
            cat_condition = "And pc.id_brand = '"+str(cat)+"' "
        request = ("select SUM(sl.price_subtotal) "+
                    "From sale_order s "+
                    "Join account_move a on a.invoice_origin = s.name "
                    "Join sale_order_line sl on s.id = sl.order_id "+
                    "Join product_product pp on pp.id = sl.product_id "+
                    "Join product_template pt on pt.id = pp.product_tmpl_id "
                    "Join product_category pc on pc.id = pt.categ_id "+
                    "WHERE (select TO_CHAR(max(date_done), 'YYYY MM') "+
                    "		from sale_order ss "+
                    "		join stock_picking ssp on ssp.origin = ss.name "+
                    "		where ss.name = s.name) = '" + self._year + " " + self._month + "' "+
                    "AND (select COUNT(ssp.state) "+
                    "	from sale_order ss "+
                    "	join stock_picking ssp on ssp.origin = ss.name "+
                    "	where ss.name = s.name) "+
                    "	= "+
                    "	(select COUNT(ssp.state) "+
                    "	from sale_order ss "+
                    "	join stock_picking ssp on ssp.origin = ss.name "+
                    "	where ss.name = s.name and ssp.state = 'done') "+
                    "AND s.state = 'sale' "+
                    user_condition +
                    cat_condition +
                    "And a.state = 'posted' "+
                    "group by s.state")
        self._odoo.env.cr.execute(request)
        return self._odoo.env.cr.fetchall()

    def get_goal_sale_oders(self,user_id,cat_id):
        user_condition = ""
        cat_condition = ""
        if str(user_id) != "all":
            user_condition = "AND u.id = '" + str(user_id) + "' "
        if cat_id :
            cat_condition = "AND bg.brand_id = '" + str(cat_id) + "' "
        request = ("select SUM(bg.goal), y.year AS Year, m.month AS Month " +
                   "From bi_finance_monthly_goal_employee e "
                   "JOIN bi_finance_brand_goal bg on bg.monthly_goal_employee_id = e.id "+
                   cat_condition +
                   "JOIN bi_finance_monthly_goal m on m.id = e.monthly_goal_id " +
                   "JOIN bi_finance_yearly_goal y on y.id = m.yearly_goal_id " +
                   "JOIN res_users u on u.id = e.commercial_id " +
                   "JOIN res_partner p on p.id = u.partner_id " +
                   "WHERE y.year = '" + self._year + "' " +
                   "AND m.month = '" + self._month + "' " +
                    user_condition+
                   "GROUP BY Year,Month")
        self._odoo.env.cr.execute(request)
        return self._odoo.env.cr.fetchall()

    def get_all_categories(self):
        request = ("select b.id, b.name_brand "+
                   "From bi_finance_brand b")
        self._odoo.env.cr.execute(request)
        return self._odoo.env.cr.fetchall()

    def get_sale_oders_forecast(self,user_id):
        condition = ""
        if str(user_id) != "all":
            condition = "And s.user_id = '" + str(user_id) + "' "
        request = ("select SUM(s.amount_untaxed), TO_CHAR(s.commitment_date, 'YYYY') AS Year, " +
                   "TO_CHAR(s.commitment_date, 'MM') AS Month " +
                   "From sale_order s " +
                   "WHERE TO_CHAR(s.commitment_date, 'YYYY MM') = '" + self._year + " " + self._month + "' " +
                   "AND s.state = 'sale' " +
                   condition +
                   "GROUP BY Year,Month ")
        self._odoo.env.cr.execute(request)
        return self._odoo.env.cr.fetchall()

    # récupère tout user id ayant un objectif sur le CA
    def get_user_id_have_goal(self):
        request = ("select Distinct(u.id), p.name AS Employee " +
                   "From bi_finance_monthly_goal_employee e " +
                   "JOIN bi_finance_monthly_goal m on m.id = e.monthly_goal_id " +
                   "JOIN bi_finance_yearly_goal y on y.id = m.yearly_goal_id " +
                   "JOIN res_users u on u.id = e.commercial_id " +
                   "JOIN res_partner p on p.id = u.partner_id " +
                   "WHERE y.year = '" + self._year + "' ")
        self._odoo.env.cr.execute(request)
        return self._odoo.env.cr.fetchall()

    def get_name_employee(self,user_id):
        request = (
            "select p.name "
            "From res_users u " +
            "JOIN res_partner p on p.id = u.partner_id "+
            "WHERE u.id = '"+str(user_id)+"' "
        )
        self._odoo.env.cr.execute(request)
        return self._odoo.env.cr.fetchone()

    def get_sale_oders_ind_sql(self, str_ids):
        request = ("select s.user_id, SUM(s.amount_untaxed)" +
                   "From sale_order s " +
                   "WHERE s.commitment_date IS NULL " +
                   "AND s.state = 'sale' " +
                   "And s.user_id in (" + str(str_ids) + ") " +
                   "group by s.user_id")
        self._odoo.env.cr.execute(request)
        return self._odoo.env.cr.fetchone()