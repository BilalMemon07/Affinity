# -*- coding: utf-8 -*-
{
    'name': "Product APP",
    'summary': """Customer Product for CRM""",
    'description': """""",
    'author': "Bilal Memon",
    'website': "",
    'category': 'Specific Industry Applications',
    'version': '0.1',
    'depends': ['crm', 'account','product'],
    'data': [
        'security/ir.model.access.csv',
        'views/views.xml',
        'wizard/rejection_note.xml',
        'wizard/disbursement_payment.xml',
        'views/payment_views.xml',
        'data/dis_seq.xml',
    ],
    'license': 'AGPL-3',
    'installable': True,
    'application': True,
    'auto_install': False,
    'sequence': '-100',
}
