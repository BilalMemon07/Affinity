# -*- coding: utf-8 -*-

{
    'name': 'Odoo Global Discount on Invoice with Tax calculation',
    'version': '16.0.0.2',
    'category': 'Invoicing',
    'sequence': 14,
    'price': 25,
    'currency': "EUR",
    'summary': 'invoice discount with tax invoices discount purchase discount purchase order discount fixed discount on vendor bill invoice discount vendor discount on purchase vendor bill discount All in one Discount after tax amount global discount before tax amount',
    'description': """
Manage sales and purchase orders and Invoice Discount Manages the Discount in Sale order , Purchase Order and in whole Sale order/Purchase order basis on Fix
and Percentage wise as well as calculate tax before discount and after

discount and same for the Invoice.
discount on sale purchase invoice with tax
discount with tax on Sale Purchase Invoice Discount
Sale Purchase Invoice Discount
tax calculation with discount 
sale discount
purchase discount
Invoice Discount
discount with tax
tax without discount
Discount on Sale Order
Discount On Purchase Order
discount on purchase orderline
Discount on Sale Orderline
Discount on Invoice Line (Invoices & Bills)
Account Discount
customer discount

""",

    'author': 'Bilal Memon',
    'website': '',
    'images': [],
    'depends': ['base','sale','sale_management','account','stock'],
    'data': [
        'views/invoice_view.xml',
        'report/inherit_account_report.xml',
        
    ],
    'installable': True,
    'auto_install': False,
    'application': True,
    'live_test_url': "",
    'images':[],
    'license': 'LGPL-3',
}

