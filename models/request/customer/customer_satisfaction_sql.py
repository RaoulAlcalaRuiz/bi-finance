class CustomerSatisfactionSql:
    def __init__(self,id_company,year,id_goal,odoo):
        self._id_company = id_company
        self._id_goal = id_goal
        self._year = year
        self._month = 0
        self._odoo = odoo

    def set_month(self, month):
        self._month = month

    def get_goal_otd(self):
        request = ("select m.goal_percentage_in_time " +
                   "from bi_finance_yearly_goal y " +
                   "join bi_finance_monthly_goal m on m.yearly_goal_id = y.id " +
                   "where y.id = '" + str(self._id_goal) + "' and m.month = '" + str(self._month) + "' ")
        self._odoo.env.cr.execute(request)
        return self._odoo.env.cr.fetchall()

    def get_time_delivery(self):
        request = ("select m.day_before_delivery " +
                   "from bi_finance_yearly_goal y " +
                   "join bi_finance_monthly_goal m on m.yearly_goal_id = y.id " +
                   "where m.month = '" + str(self._month) + "' AND y.id = '" + str(self._id_goal) + "' ")
        self._odoo.env.cr.execute(request)
        return self._odoo.env.cr.fetchall()

    def get_count_month_delivery_in_time(self, time_delivery):
        time = -time_delivery
        request = ("select count(o.id) " +
                   "From sale_order o " +
                   "JOIN res_company c on c.id = o.company_id " +
                   "WHERE TO_CHAR(o.commitment_date,'YYYY') = '" + str(self._year) + "' " +
                   "AND CAST (TO_CHAR(o.commitment_date,'MM') AS INTEGER) = '" + str(self._month) + "' " +
                   "AND o.state = 'sale' " +
                   "AND c.id = '" + str(self._id_company) + "' " +
                   "AND date_part('day',age(o.commitment_date, o.effective_date)) > '" + str(time) + "'")
        self._odoo.env.cr.execute(request)
        return self._odoo.env.cr.fetchall()

    def get_count_month_delivery(self):
        request = ("select count(o.id) " +
                   "From sale_order o " +
                   "JOIN res_company c on c.id = o.company_id " +
                   "WHERE TO_CHAR(o.commitment_date,'YYYY') = '" + str(self._year) + "' " +
                   "AND CAST (TO_CHAR(o.commitment_date,'MM') AS INTEGER) = '" + str(self._month) + "' " +
                   "AND o.state = 'sale' " +
                   "AND c.id = '" + str(self._id_company) + "' ")
        self._odoo.env.cr.execute(request)
        return self._odoo.env.cr.fetchall()

    def get_goal_oqd(self):
        request = ("select m.quality " +
                   "From bi_finance_yearly_goal y " +
                   "JOIN bi_finance_monthly_goal m on y.id = m.yearly_goal_id " +
                   "WHERE y.year = '" + str(self._year) + "' " +
                   "AND m.month = '" + str(self._month) + "'")
        self._odoo.env.cr.execute(request)
        return self._odoo.env.cr.fetchall()

    def get_quality_delivery(self, bad_quality):
        month_formatted = "{:02d}".format(self._month)
        request = ("select COUNT(s.problematic_quality) as Good " +
                   "From sale_order s  " +
                   "WHERE TO_CHAR(s.commitment_date, 'YYYY MM') = '" + str(self._year) + " " + str(month_formatted) + "' " +
                   "AND s.effective_date is not NULL " +
                   "AND s.problematic_quality = '" + bad_quality + "' " +
                   "AND s.state = 'sale' ")
        self._odoo.env.cr.execute(request)
        return self._odoo.env.cr.fetchall()