# -*- coding: utf-8 -*-
from odoo import fields, models,api
from ..classes.date_delivery import DateDeliveryOne

class Order(models.Model):
    _inherit = 'sale.order'

    # Date de livraison prévue => overide pour qui soit modifiable même en bon de commande
    commitment_date = fields.Datetime('Delivery Date',
                                      states={'draft': [('readonly', False)],
                                              'sent': [('readonly', False)],
                                              'sale': [('readonly', False)]}
                                      )

    justification_for_delay = fields.Char(
        string="Justification de retard",
        help="Justification de retard. Peut être complété uniquement si la livraison est en retard." )

    delivery_late = fields.Integer(string="Etat de livraison",compute="_delivering_state")
    is_late = fields.Boolean(string="Retard",
                             compute="_delivering_late",
                             store=True,
                             help="État de la livraison. Si la case est cochée, la livraison est en retard. Si la case n'est pas cochée, la livraison est arrivée à temps ou la livraison n'a pas encore eu lieu mais à de l'avance ")

    problematic_quality = fields.Boolean(string="Qualité problématique",
                                         default=False,
                                         help="Qualité du produit livré. Peut être cochée uniquement si la livraison est considérée envoyée.")
    justification_quality = fields.Char(
        String="Justification de qualité",
        help="Justification de la mauvaise qualité des produits livrés. Peut être complété uniquement si la livraison est considérée de mauvaise qualité." )

    # si la livraison est en retard delivery_late = -1 si on ne sais pas encore = 0 et si elle est livrée à temps = 1
    @api.depends('effective_date', 'commitment_date')
    def _delivering_state(self):
        for r in self:
            delta = 0
            if r.commitment_date:
                delta = self._get_day_before_delivering(r.commitment_date.year, r.commitment_date.month)
            date_object = DateDeliveryOne(r.commitment_date, self._get_effective_date(r.name), delta)
            r.delivery_late = date_object.delivery_in_time()


    @api.depends('delivery_late')
    def _delivering_late(self):
        for r in self:
            if r.delivery_late == -1 :
                r.is_late = True
            else :
                r.is_late = False

    def _get_effective_date(self,name):
        request=("select "+
                    "(select max(date_done) "+
                    "from sale_order ss "+
                    "join stock_picking ssp on ssp.origin = ss.name  "+
                    "where ss.name = o.name) as Effective_date "+
                "From sale_order o "+
                "Where o.name = '"+str(name)+"'"+
                 "AND (select COUNT(ssp.state) " +
                 "	from sale_order ss " +
                 "	join stock_picking ssp on ssp.origin = ss.name " +
                 "	where ss.name = o.name) " +
                 "	= " +
                 "	(select COUNT(ssp.state) " +
                 "	from sale_order ss " +
                 "	join stock_picking ssp on ssp.origin = ss.name " +
                 "	where ss.name = o.name and ssp.state = 'done') ")

        self.env.cr.execute(request)
        result = self.env.cr.fetchone()
        if result is not None:
            return result[0]
        else:
            return None

    def _get_day_before_delivering(self,year, month):
        request=("select m.day_before_delivery "+
                    "from bi_finance_yearly_goal y  "+
                    "join bi_finance_monthly_goal m on y.id = m.yearly_goal_id  "+
                    "where y.year = '"+str(year)+"' AND m.month = '"+str(month)+"'")

        self.env.cr.execute(request)
        result = self.env.cr.fetchone()
        if result is not None:
            return result[0]
        else:
            return 0