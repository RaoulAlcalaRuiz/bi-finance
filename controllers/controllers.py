# -*- coding: utf-8 -*-
# from odoo import http


# class BiFinance(http.Controller):
#     @http.route('/bi_finance/bi_finance/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/bi_finance/bi_finance/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('bi_finance.listing', {
#             'root': '/bi_finance/bi_finance',
#             'objects': http.request.env['bi_finance.bi_finance'].search([]),
#         })

#     @http.route('/bi_finance/bi_finance/objects/<model("bi_finance.bi_finance"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('bi_finance.object', {
#             'object': obj
#         })
