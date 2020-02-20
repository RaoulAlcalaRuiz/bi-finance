# -*- coding: utf-8 -*-
{
    'name': "BI Finance",

    'summary': """
        Module permettant de réaliser des objectifs finacier et de les comparer à la réalité
        """,

    'description': """
        Module permettant de réaliser des objectifs finacier et de les comparer à la réalité
    """,

    'author': "Aquatic Science SA - Raoul Alcala Ruiz",
    'website': "https://www.aquatic-science.be/",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/13.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'Business Intelligence',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['base'],

    # always loaded
    'data': [
        'security/security.xml',
        'security/ir.model.access.csv',
        'views/yearly_goal.xml',
        'views/monthly_goal.xml',
        'views/monthly_goal_employee.xml',
        'views/menu.xml',
        'reports.xml',
    ],
    # only loaded in demonstration mode
    'demo': [
        'demo/demo.xml',
    ],
    'application':True,
}
