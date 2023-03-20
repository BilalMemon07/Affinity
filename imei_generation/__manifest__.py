# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

{
    'name': 'IMEI Generation',
    'version': "1.0.0",
    # 'category': 'Purchase',
    'summary': '',
    'description': """""",
    # 'sequence': '-100',
    'depends': ['purchase','sale','stock'],
    'data': [
        'views/imei_generation_view.xml',
        'security/ir.model.access.csv',
        'data/imei_generation_sequence.xml',
        ],
    'demo': [],
    'qweb': [],
     'installable': True,
    'application': True,
    'auto_install': False,
    'License': 'LGPL-3'
}
