class CustomerSatisfactionSql:
    def __init__(self,id_company,year,id_goal,odoo):
        self._id_company = id_company
        self._id_goal = id_goal
        self._year = year
        self._month = 0
        self._odoo = odoo

    def set_month(self, month):
        self._month = month

    # Revoi l'objectif en pourcentage de livraison arrivé à temps
    def get_goal_otd(self):
        request = ("select m.goal_percentage_in_time " +
                   "from bi_finance_yearly_goal y " +
                   "join bi_finance_monthly_goal m on m.yearly_goal_id = y.id " +
                   "where y.id = '" + str(self._id_goal) + "' and m.month = '" + str(self._month) + "' ")
        self._odoo.env.cr.execute(request)
        return self._odoo.env.cr.fetchall()

    # Revoi la durée de livraison d'avance
    def get_time_delivery(self):
        request = ("select m.day_before_delivery " +
                   "from bi_finance_yearly_goal y " +
                   "join bi_finance_monthly_goal m on m.yearly_goal_id = y.id " +
                   "where m.month = '" + str(self._month) + "' AND y.id = '" + str(self._id_goal) + "' ")
        self._odoo.env.cr.execute(request)
        return self._odoo.env.cr.fetchall()

    # Revoi le nombre de livraison livré à temps
    def get_count_month_delivery_in_time(self, time_delivery):
        request = ("select COUNT(o.id) "+
                    "From sale_order o "+
                    "JOIN res_company c on c.id = o.company_id "+
                    "WHERE TO_CHAR(o.commitment_date,'YYYY') = '" + str(self._year) + "' "+
                    "AND CAST (TO_CHAR(o.commitment_date,'MM') AS INTEGER) = '" + str(self._month) + "' "+
                    "AND o.state = 'sale' "+
                    "AND c.id = '" + str(self._id_company) + "' "+
                    "AND date_part('day', "+
                    "	age( "+
                    "		DATE(o.commitment_date), "+
                    "		DATE( "+
                    "			(select max(date_done) "+
                    "			from sale_order ss "+
                    "			join stock_picking ssp on ssp.origin = ss.name "+
                    "			where ss.name = o.name) "+
                    "		) "+
                    "	) "+
                    ") > INTEGER '" + str(time_delivery) + "' "+
                    "AND (select COUNT(ssp.state) "+
                    "	from sale_order ss "+
                    "	join stock_picking ssp on ssp.origin = ss.name "+
                    "	where ss.name = o.name) "+
                    "	= "+
                    "	(select COUNT(ssp.state) "+
                    "	from sale_order ss "+
                    "	join stock_picking ssp on ssp.origin = ss.name "+
                    "	where ss.name = o.name and ssp.state = 'done')")
        self._odoo.env.cr.execute(request)
        return self._odoo.env.cr.fetchall()

    # Revoi le nombre de bon de commande sur le mois
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
                   "WHERE TO_CHAR(s.effective_date, 'YYYY MM') = '" + str(self._year) + " " + str(month_formatted) + "' " +
                   "AND s.problematic_quality = '" + bad_quality + "' " +
                   "AND s.state = 'sale' ")
        self._odoo.env.cr.execute(request)
        return self._odoo.env.cr.fetchall()