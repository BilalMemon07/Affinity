# -*- coding: utf-8 -*-
{
    'name': "Affinity X Youniform Extension",

    'summary': """
        Short (1 phrase/line) summary of the module's purpose, used as
        subtitle on modules listing or apps.openerp.com""",

    'description': """
        Long description of module's purpose
    """,
    'sequence': 10,
    'author': "Bilal(Sr. Odoo Developer)",
    'website': "",

    'category': 'Sales',
    'version': '0.1',
    'license': 'LGPL-3',

    'installable': True,
    'application': True,
    
    'depends': ['base','sale','stock','product'],

    
    'data': [
        'views/commission_view.xml',
        
    ],
    
    'demo': [
        'demo/demo.xml',
    ],
}
