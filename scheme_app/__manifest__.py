# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

{
    'name': 'Scheme',
    'version': "1.0.0",
    'category': 'All',
    'summary': '',
    'description': """""",
    'sequence': '-100',
    'depends': ['product','base','sale','stock'],
    'data': [
        'views/scheme_view.xml',
        'security/ir.model.access.csv',
        # 'data/gate_sequence.xml',
        ],
    'demo': [],
    'qweb': [],
    'images' : ['static/description/icon.png'],
    'installable': True,
    'application': True,
    'auto_install': False,
    'License': 'LGPL-3'
}
