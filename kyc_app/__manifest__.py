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
    'depends': ['base'],
    'data': [
        'security/ir.model.access.csv',
        'views/views.xml',
        'wizards/rejection_note_kyc.xml',
    ],
    'license': 'AGPL-3',
    'license': 'AGPL-3',
    'installable': True,
    'application': True,
    'auto_install': False,
    'sequence': '-100',
}
