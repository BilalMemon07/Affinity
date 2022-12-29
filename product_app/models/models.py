# -*- coding: utf-8 -*-
from odoo import models, fields, api, _
from odoo.exceptions import UserError

    
class Leads(models.Model):
    _inherit = 'crm.lead'

    product_type = fields.Selection([('1', 'Broker Lending'), ('2', 'Drive Throught Lending'),('3', 'Invoice Discounting')], string='Product Type', required=True) 
    # For Broker Landing
    limit_request = fields.Float(string= "limit Request") #for (b)
    requested_amount = fields.Float(string= "Requested Amount") #for (b/d)
    instrument_number = fields.Float(string= "Instrument Number") #for (b/d)
    instrument_number = fields.Float(string= "Instrument Number") #for (b/d)
    facility_request_date = fields.Date(string= "Facility Request date") #for (b/d)
    instrument_due_date = fields.Date(string= "Instrument due date") #for (b/d)
    attachment = fields.Date(string= "Attachment") #for (b/d)

