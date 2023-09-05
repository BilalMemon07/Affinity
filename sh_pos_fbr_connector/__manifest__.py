# -*- coding: utf-8 -*-
# Part of Softhealer Technologies.
{
    "name": "POS FBR Connector",
    
    "author": "Softhealer Technologies",
    
    "website": "https://www.softhealer.com",

    "support": "support@softhealer.com",
        
    "version": "16.0.1",
    
    "category": "Point Of Sale",
    
    "summary": "Send POS Detail To FBR, Filter FBR Data Module, Sync FBR Data, Fetch PCT Code In FBR App, Connect FBR Portal With POS Odoo, Federal Board of Revenue Odoo Connector, FBR Odoo Sync, Odoo FBR, Odoo FBR Connector, Pakistan Odoo, Odoo Pakistan",
        
    "description": """  
This module will help to send pos order details to the FBR portal, It's auto-send order information to be on payment done from pos and receipt generated, receipt generated with invoice no. which is fetched from FBR Portal, If any issue with FBR portal connection than it will auto resend using a cron job or manually as well from the backend. It will not show invoice no if the FBR Portal connection issue. You can easily filter failed/success sync orders of FBR Portal. It also provides PCT(Pakistan Customs Tariff) code.

ABOUT FBR :

The Federal Board of Revenue (FBR) formerly known as the Central Board of Revenue (CBR), is a top federal government organization of Pakistan that investigates tax crimes and money-laundering. FBR operates through special Broadening of Tax Base Zones that keep tax evaders under surveillance and perform special tasks for FBR Headquarters. FBR performs the role of collection of taxation in the country from all individuals and businesses.
FBR also collects intelligence on tax evasion and administers tax laws for the Government of Pakistan and acts as the central revenue collection agency of Pakistan.

POS Federal Board of Revenue Connector Odoo
 Send POS Detail To FBR Module, Filter FBR Data, Sync Federal Board of Revenue Data, Fetch PCT Code In FBR, Resend Data Using Cronjob, Connect FBR Portal With POS Odoo.
 Send POS Detail To FBR, Filter FBR Data Module, Sync FBR Data, Fetch PCT Code In FBR App, Resend Data Using Cronjob, Connect FBR Portal With POS Odoo, FBR Odoo, Federal Board of Revenue Odoo Connector, FBR Odoo Sync, Odoo FBR, Odoo FBR Connector, Pakistan Odoo, Odoo Pakistan.""",
     
    "depends": ['point_of_sale','base','web'],
    
    "data": [
        "views/views.xml",
        "data/data.xml",
        "views/templates.xml",
    ],
    'assets': {
        'point_of_sale.assets': [
            '/sh_pos_fbr_connector/static/src/js/pos.js',
            '/sh_pos_fbr_connector/static/src/js/pos_fbr_product.js',
        ],
    }, 
    "qweb":["static/src/xml/*.xml"],
    "installable": True,
    "auto_install": False,
    "application": True,    
    'images': ['static/description/background.png', ],
    "live_test_url": "https://youtu.be/BDxnPI1zvos",
    "price": 150,
    "currency": "EUR"    
}
