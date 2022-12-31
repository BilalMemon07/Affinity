# -*- coding: utf-8 -*-
from odoo import models, fields, api, _
from odoo.exceptions import UserError

    
class Leads(models.Model):
    _inherit = 'crm.lead'

    product_type = fields.Selection([('1', 'Broker Lending'), ('2', 'Drive Throught Lending'),('3', 'Invoice Discounting')], string='Product Type', required=True) 
    limit_request = fields.Float(string= "limit Request") #for (b)
    requested_amount = fields.Float(string= "Requested Amount") #for (b/d)
    instrument_number = fields.Float(string= "Instrument Number") #for (b/d)
    instrument_number = fields.Float(string= "Instrument Number") #for (b/d)
    facility_request_date = fields.Date(string= "Facility Request date") #for (b/d/i)
    instrument_due_date = fields.Date(string= "Instrument due date") #for (b/d/i)
    attachment = fields.Binary(string= "Attachment") #for (b/d)

    # for invoice
    select_party = fields.Char(string="Select Party (coporate)") #for (i)
    invoice_amount = fields.Float(string="Invoice Amount") #for (i)
    tag_trip = fields.Float(string="Tag Trip") #for (i)
    invoice_type = fields.Selection([('1', 'Transportation Invoice'), ('2', 'Good Invoice')], string='Invoice Type', required=True) #for (i)
    description = fields.Text(string="Description") #for (i)
    invoice_attachment = fields.Binary(string= "Upload Invoice") #for (i)

