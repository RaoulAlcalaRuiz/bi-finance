class StockSql:
    def __init__(self, year, company_id, odoo):
        self._year = str(year)
        self._company_id = str(company_id)
        self._month = '0'
        self._odoo = odoo

    def set_month(self, month):
        self._month = str(month)

    def get_stock_value(self,cat=None):
        cat_condition = ""
        if cat :
            cat_condition = "and pc.id_brand = '"+str(cat)+"' "

        request = ("select " +
                   "sum( " +
                   "	CASE " +
                   "		  WHEN s.sale_line_id IS NOT NULL  THEN -s.product_uom_qty " +
                   "		  WHEN s.sale_line_id IS NULL AND s.purchase_line_id IS NULL AND s.location_id = 8 THEN -s.product_uom_qty " +
                   "		  ELSE s.product_uom_qty " +
                   "	END " +
                   ") *  " +
                   "CASE  " +
                   "	  WHEN ip.value_float IS NULL THEN 1 " +
                   "	  ELSE ip.value_float " +
                   "END	 AS stock_value " +
                   "from stock_move s " +
                   "join product_product p on p.id = s.product_id " +
                   "join product_template pt on pt.id = p.product_tmpl_id "+
                   "join product_category pc on pc.id = pt.categ_id " +
                   "left outer join ir_property ip on ip.name = 'standard_price'  " +
                   "	and CAST(substring(ip.res_id,POSITION(',' IN ip.res_id)+1) as INTEGER) = p.id " +
                   "where state = 'done' " +
                   "	and s.company_id = '"+self._company_id+"' " +
                   "	and CAST (TO_CHAR(date,'YYYY') as INTEGER) <= '"+self._year+"' AND CAST (TO_CHAR(date,'MM') as INTEGER) <= '"+self._month+"' " +
                   cat_condition+
                   "group by s.product_id, ip.value_float")
        self._odoo.env.cr.execute(request)
        return self._odoo.env.cr.fetchall()

    def get_goal_stock_value(self, cat = None):
        cat_condition = ""
        if cat:
            cat_condition = "AND bg.brand_id = '"+str(cat)+"' "
        request = ("select sum(bg.goal) "+
                    "From bi_finance_yearly_goal y  "+
                    "JOIN bi_finance_monthly_goal m on y.id = m.yearly_goal_id  "+
                    "JOIN bi_finance_brand_goal_stock bg on bg.monthly_goal_id = m.id  "+
                    "WHERE y.year = '2020' "+
                    "AND m.month = '1' "+
                    cat_condition)
        self._odoo.env.cr.execute(request)
        return self._odoo.env.cr.fetchall()
