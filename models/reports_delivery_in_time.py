from odoo import models, api
from datetime import datetime

from ..classes.date_delivery import DateDelivery, compute_achievement


class ReportGoalEmployee(models.AbstractModel):
    _name = 'report.bi_finance.delivery_in_time_report_template'

    @api.model
    def _get_report_values(self, docids, data=None):
        yearly_goal = self._get_current_year(docids)
        year = yearly_goal.year
        currency_id = self.env.ref('base.main_company').currency_id
        id_company = self._get_id_company(docids)

        # Norma data
        list_in_time = self._get_each_month_in_time(id_company,year,docids[0])
        list_in_time_accrued = self._compute_delivery_accrued(id_company,year,docids[0])
        percent_wanted = self._get_percent_each_month(docids[0])

        # Formated data for show it
        list_in_time_formated = self._formated_all_percent(list_in_time)
        list_in_time_accrued_formated = self._formated_all_percent(list_in_time_accrued)
        percent_wanted_formated = self._formated_all_percent(percent_wanted)

        # Null value
        nullList = DateDelivery(list_in_time_formated,year)
        list_in_time_formated = nullList.new_list

        nullList.change_list(list_in_time_accrued_formated)
        list_in_time_accrued_formated = nullList.new_list

        nullList.change_list(list_in_time)
        list_in_time = nullList.new_list

        nullList.change_list(list_in_time_accrued)
        list_in_time_accrued = nullList.new_list

        #ux data
        goal_achieved = compute_achievement(list_in_time,percent_wanted)

        docargs = {
            'year': yearly_goal.year,
            'currency_id': currency_id,
            'zero_value': 0,
            'list_in_time':list_in_time,
            'list_in_time_accrued':list_in_time_accrued,
            'percent_wanted':percent_wanted,
            'list_in_time_formated':list_in_time_formated,
            'list_in_time_accrued_formated':list_in_time_accrued_formated,
            'percent_wanted_formated':percent_wanted_formated,
            'goal_achieved':goal_achieved,
            'doc_model': 'bi_finance.yearly_goal'
        }
        return docargs

    def _get_current_year(self,id):
        return self.env['bi_finance.yearly_goal'].browse(id)

    def _get_id_company(self,id):
        return self.env['bi_finance.yearly_goal'].search([("id","in",id)])[0].company_id.id

    def _get_percent_each_month(self,id_year):
        new_list = []
        for month in range(1,13):
            new_list.append(self._get_precent_goal(id_year, month))
        return new_list

    def _get_each_month_in_time(self,company_id, year,id_year):
        new_list = []
        for month in range(1,13):
            time_delivery = self._get_time_delivery(id_year,month)
            result_in_time = self._get_count_month_delivery_in_time(time_delivery, company_id, month, year)
            result_count = self._get_count_month_delivery( company_id, month, year)
            new_list.append(self._average_delivery(result_in_time,result_count))
        return new_list

    def _compute_delivery_accrued(self ,company_id, year,id_year):
        new_list = []
        result_in_time = 0
        result_count = 0
        for month in range(1,13):
            real_month = month
            time_delivery = self._get_time_delivery(id_year,real_month)
            result_in_time += self._get_count_month_delivery_in_time(time_delivery, company_id, real_month, year)
            result_count += self._get_count_month_delivery( company_id, real_month, year)
            new_list.append(self._average_delivery(result_in_time,result_count))
        return new_list

    def _get_count_month_delivery_in_time(self,time_delivery ,company_id ,month, year):
        time = -time_delivery
        request =("select count(o.id) "+
                    "From sale_order o "+
                    "JOIN res_company c on c.id = o.company_id "+
                    "WHERE TO_CHAR(o.commitment_date,'YYYY') = '"+str(year)+"' "+
                    "AND CAST (TO_CHAR(o.commitment_date,'MM') AS INTEGER) = '"+str(month)+"' "+
                    "AND o.state = 'sale' "+
                    "AND c.id = '"+str(company_id)+"' "+
                    "AND date_part('day',age(o.commitment_date, o.effective_date)) > '"+str(time)+"'")
        self.env.cr.execute(request)
        result = self.env.cr.fetchall()

        if len(result) != 0:
            result = result[0][0]
        else:
            result = 0
        return result

    def _get_count_month_delivery(self,company_id ,month, year):
        request =("select count(o.id) "+
                    "From sale_order o "+
                    "JOIN res_company c on c.id = o.company_id "+
                    "WHERE TO_CHAR(o.commitment_date,'YYYY') = '"+str(year)+"' "+
                    "AND CAST (TO_CHAR(o.commitment_date,'MM') AS INTEGER) = '"+str(month)+"' "+
                    "AND o.state = 'sale' "+
                    "AND c.id = '"+str(company_id)+"' ")
        self.env.cr.execute(request)
        result = self.env.cr.fetchall()

        if len(result) != 0:
            result = result[0][0]
        else:
            result = 0
        return result

    def _get_time_delivery(self,id_year,month):
        request = ("select m.day_before_delivery "+
                    "from bi_finance_yearly_goal y "+
                    "join bi_finance_monthly_goal m on m.yearly_goal_id = y.id "+
                    "where m.month = '"+str(month)+"' AND y.id = '"+str(id_year)+"' ")
        self.env.cr.execute(request)
        result = self.env.cr.fetchone()
        if result is not None:
            return result[0]
        else:
            return 0

    def _get_precent_goal(self,id_year,month):
        request =("select m.goal_percentage_in_time "+
                    "from bi_finance_yearly_goal y "+
                    "join bi_finance_monthly_goal m on m.yearly_goal_id = y.id "+
                    "where y.id = '"+str(id_year)+"' and m.month = '"+str(month)+"' ")
        self.env.cr.execute(request)
        result = self.env.cr.fetchone()
        if result is not None:
            return result[0]
        else:
            return 0

    def _average_delivery(self,in_time, count):
        result = 0
        if count == 0:
            if (count == 0 & in_time != 0):
                result = 100
        else:
            result = in_time / count * 100
        return result

    def _format_percent(self,value):
        return "{:4.1f} %".format(value)

    def _formated_all_percent(self, list):
        new_list = []
        for value in list:
            new_list.append(self._format_percent(value))
        return new_list


