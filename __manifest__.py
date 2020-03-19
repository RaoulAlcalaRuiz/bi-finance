# -*- coding: utf-8 -*-
{
    'name': "Module Décisionnel",

    'summary': """
        Module permettant de réaliser des objectifs finacier et de les comparer à la réalité
        """,

    'description': """
        Module permettant de réaliser des objectifs finacier et de les comparer à la réalité
    """,

    'author': "Aquatic Science SA - Raoul Alcala Ruiz",
    'website': "https://www.aquatic-science.be/",

    'images': [
        'static/src/img/icon.png',
        'static/src/img/logo1.png',
    ],

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/13.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'Business Intelligence',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['base','sale_management','percent_field','stock','account'],

    # always loaded
    'data': [
        'security/security.xml',
        'security/ir.model.access.csv',
        'reports/reports.xml',
        'reports/reports_delivery.xml',
        'reports/reports_employee.xml',
        'reports/reports_stock.xml',
        'views/yearly_goal.xml',
        'views/yearly_goal_delivery.xml',
        'views/yearly_goal_employee.xml',
        'views/monthly_goal.xml',
        'views/monthly_goal_employee.xml',
        'views/menu.xml',
        'views/sale_order.xml',
    ],
    # only loaded in demonstration mode
    'demo': [
        'demo/demo.xml',
    ],
    'application':True,
}
