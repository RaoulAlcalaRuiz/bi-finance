from odoo import models, api

from .request.sale_order import get_sale_oders_user
from .request.sale_order_forecast import get_sale_oders_forecast
from .request.sale_order_goal import get_goal_of_user
from .request.sale_order_ind import get_sale_oders_ind_sql
from ..classes.average import AverageList, Average


def _compute_annual_sales(self, year, user):
    employee_goal = []
    for i in range(1, 13):
        goal = get_sale_oders_user(self, year, "{:02d}".format(i), user)
        if len(goal) != 0:
            employee_goal.append(goal[0][0])
        else:
            employee_goal.append(0)
    return employee_goal

def _compute_annual_sales_forecast(self, year, user):
    employee_goal = []
    for i in range(1, 13):
        goal = get_sale_oders_forecast(self, year, "{:02d}".format(i), user)
        if len(goal) != 0:
            employee_goal.append(goal[0][0])
        else:
            employee_goal.append(0)
    return employee_goal

def _compute_goal(self, year,user):
    employee_goal = []
    for i in range(1, 13):
        goal = get_goal_of_user(self,user,year, str(i))
        if len(goal) != 0:
            employee_goal.append(goal[0][0])
        else:
            employee_goal.append(0)
    return employee_goal

def _compute_sum_data(employe_goal_annual_sales,employe_annual_sales,year):
    sum_employe_goal = AverageList(employe_goal_annual_sales).sum_data_1d()
    sum_employe_real = AverageList(employe_annual_sales).sum_data_1d()
    sum_employe_average = Average(sum_employe_real,sum_employe_goal).get_pourcentage_formated()
    sum_employe_average_in_time = Average(sum_employe_real,sum_employe_goal).compute_in_time_average_year(year)
    sum_employe_annual_sales = [sum_employe_real,sum_employe_goal,sum_employe_average,sum_employe_average_in_time]
    return sum_employe_annual_sales

def _compute_average(goal,real,year):
    sum_goal = AverageList(goal).sum_data_1d()
    sum_real = AverageList(real).sum_data_1d()
    sum_employe_average = Average(sum_real,sum_goal).get_pourcentage_formated()
    return [sum_employe_average,Average(sum_real,sum_goal).compute_in_time_average_year(year)]

def _get_sale_oders_ind(self,users_id):
    str_ids = _compute_list_str(users_id)
    list_ind = get_sale_oders_ind_sql(self,str_ids)
    return _compute_return_ind(self,list_ind,str_ids)



def _compute_return_ind(self, list_ind, str_ids):
    request = ("select u.id, p.name "+
               "From res_users u "+
               "Join res_partner p on u.partner_id = p.id "+
               "WHERE u.id in ("+str_ids+")")
    self.env.cr.execute(request)
    result = self.env.cr.fetchall()
    list_ind_formated = []
    i = 0
    while i < len(result):
        j = 0
        while j < len(list_ind):
            if result[i][0] == list_ind[j][0]:
                list_ind_formated.append((result[i][1],list_ind[j][1]))
            j += 1
        i += 1
        if i != len(list_ind_formated):
            list_ind_formated.append((result[i-1][1],0))

    return list_ind_formated

def _compute_list_str(list):
    i=0
    result = ''
    while i < len(list):
        if i == 0 :
            result += '\'' + str(list[i])+'\''
        else :
            result += ',\'' + str(list[i])+'\''
        i+=1
    return result

def _get_name_user(self, user_id):
    request = ("select p.name " +
               "From res_users u " +
               "JOIN res_partner p on u.partner_id = p.id " +
               "WHERE u.id = '"+str(user_id)+"' " )
    self.env.cr.execute(request)
    return self.env.cr.fetchone()[0]

