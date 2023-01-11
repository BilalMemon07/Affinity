# -*- coding: utf-8 -*-
from odoo import models, fields, api, _
from odoo.exceptions import UserError

    
class Leads(models.Model):
    _inherit = 'crm.lead'


    state = fields.Selection([('pending', 'Pending'), ('approve', 'Approved'), ('reject', 'Reject')], string='Status', default='pending')
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

    # related_stage_name = fields.Related('stage_id','name', type="char",string="stage")
    related_stage_name = fields.Char(string='stage', related='stage_id.name')


    # for Business Team 
    bank_attachment = fields.Binary(string= "Bank Attactment")
    trip_data = fields.Binary(string= "Trip Data")
    ownership_doc = fields.Binary(string= "Truck Ownership")
    # for Business Team & Risk & Compliance

    kyc_check = fields.Boolean(string = 'Kyc check with NADRA')
    bureau_check = fields.Boolean(string = 'Credit Bureau Check')
    risk_score = fields.Float(string="Risk Score Calculation")
    assign_limit = fields.Float(string="Assign Limit")

    # for Business Team & Risk & Compliance & Management

    priority = fields.Selection([('0', 'Normal'),('1', 'Good'),('2', 'Very Good'),('3', 'Excellent')], string="Priority", default='0')
    Note = fields.Text(string="Appreciation",)
    rejection_note = fields.Text(string="Rejection Note")


    @api.model
    def create(self,vals):
        if vals.get('name', _('New')) == _('New'):
            vals['state']='pending'
        res = super(Leads,self).create(vals)
        return res


    def approve_action(self):
        if self.stage_id.id == 1:
            self['state'] = 'approve'
            self['stage_id'] = 2
            self['state'] ='pending'
        elif self.stage_id.id == 2:
            self['state'] = 'approve'
            self['stage_id'] = 3
            self['state'] ='pending'
        elif self.stage_id.id == 3:
            self['state'] = 'approve'
            # self['stage_id'] = 2
            self['state'] ='pending'
        
        # raise UserError("Helllo")

    def reject_action(self):
        if self.stage_id.id == 1:
            if self.rejection_note:
                self['state']='reject'
                self['description'] = str(self.description) + " " + str(self.rejection_note) + ' ' +'('+ str(self.related_stage_name) + ')'
                self['rejection_note'] = False
            else:
                raise UserError('Please Enter The Rejection Note')
        elif self.stage_id.id == 2:
            if self.rejection_note:
                self['state']='reject'
                self['description'] = str(self.description) + " " + str(self.rejection_note) + ' ' +'('+ str(self.related_stage_name) + ')'
                self['rejection_note'] = False
                self['stage_id'] = 1
                self['state'] ='pending'
            else:
                raise UserError('Please Enter The Rejection Note')
        elif self.stage_id.id == 3:
            if self.rejection_note:
                self['state']='reject'
                self['description'] = str(self.description) + " " + str(self.rejection_note) + ' ' + '('+ str(self.related_stage_name) + ')'
                self['rejection_note'] = False
                self['stage_id'] = 2
                self['state'] ='pending'
            else:
                raise UserError('Please Enter The Rejection Note')
        
        # raise UserError("Helllo")
    @api.onchange('product_type','partner_id')
    def partner_id_domain_pur(self):
        if self.product_type == '1': 
            return {"domain": {'partner_id': [('state', '=', 'approve')]}}
        return {"domain": {'partner_id': []}}