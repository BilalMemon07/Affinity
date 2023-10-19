# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

{
    'name': 'Record Expense',
    'version': "1.0.0",

    'author':"Syed Subhan, Bilal Memon",
    'summary': '',
    'description': """""",
    'depends': ['account','base','sale',],
    'data': [
        'views/record_expense.xml',
        'security/ir.model.access.csv',
        'data/exp_sequence.xml',
    ],
    'demo': [],
    'qweb': [],
     'installable': True,
    'application': True,
    'auto_install': False,
    'License': 'LGPL-3'
}



