from odoo import models, api


# TODO utiliser pour date_ind dans sale_order_treatment
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

def get_sale_oders_ind_sql(self, str_ids):
    request = ("select s.user_id, SUM(s.amount_untaxed)"+
                "From sale_order s "+
                "WHERE s.commitment_date IS NULL "+
                "AND s.state = 'sale' "+
                "And s.user_id in ("+str_ids+") "+
                "group by s.user_id")
    self.env.cr.execute(request)
    return self.env.cr.fetchall()