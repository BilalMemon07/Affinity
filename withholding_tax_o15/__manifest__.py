# -*- coding: utf-8 -*-
{
    'name': "Withholding Tax for Odoo v15",

    'summary': """
    Withholding tax on payments
         """,

    'description': """
        Restrict Cancel Activity Button based on user group
    """,

    'author': "Asir Amin,Muhammad Bilal",

    'category': 'Web',
    'version': '15./0.0',

    # any module necessary for this one to work correctly
    'depends': ['base', 'account'],

    # always loaded
    'data': [
        'security/ir.model.access.csv',
        'views/account_tax_view.xml',
        'views/account_payment_view.xml',
        'views/payment_register.xml'
    ],

}
