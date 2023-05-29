# -*- coding: utf-8 -*-
{
    'name': "KYC APP",

    'summary': """""",

    'description': """
        Know Your Customer.
    """,

    'author': "Bilal Memon",
    'website': "",
    'category': 'Specific Industry Applications',
    'version': '0.1',
    'depends': ['base','crm','residence_app', 'product_app'],
    'data': [
        'security/ir.model.access.csv',
        'wizards/rejection_note_kyc.xml',
        'views/views.xml',
    ],
    'license': 'AGPL-3',
    'license': 'AGPL-3',
    'installable': True,
    'application': True,
    'auto_install': False,
    'sequence': '-100',
}
