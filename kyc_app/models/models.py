# -*- coding: utf-8 -*-
from odoo import models, fields, api, _
from odoo.exceptions import UserError

    
class Partner(models.Model):
    _inherit = 'res.partner'

    rejection_note = fields.Text(String ="Rejection Note")
    state = fields.Selection([('pending', 'Pending'), ('approve', 'Approved'),('DTL_approve', 'DTL Approved'), ('reject', 'Reject')],default='pending' ,string='Status')
    # customer_name = fields.Char(string='Customer Name')
    product_type = fields.Selection([('1', 'BL'), ('2', 'DTL'),('3', 'Invoice Discounting')], string='Product Type')
    gender = fields.Selection([('male', 'Male'), ('female', 'Female')], string='Gender', required=True)
    cnic_number = fields.Char(string='CNIC Number', required=True)
    father_name = fields.Char(string='Father Name', required=True)
    cnic_expiry_date = fields.Date(string='CNIC Expiry Date', required=True)
    date_of_birth = fields.Date(string='Date of Birth', required=True)
    birth_place = fields.Char(string='Birth Place', required=True)
    mailing_address = fields.Char(string='Mailing Address', required=True)
    permanent_address = fields.Char(string='Permanent Address', required=True)
    city = fields.Char(string='City', required=True)
    province = fields.Char(string='Provice', required=True)
    nature_of_business = fields.Char(string='Nature of Business', required=True)
    requestor_income = fields.Float(string= "Requestor's Income (Monthly)", required=True)
    no_of_years = fields.Integer(string= "No of years in Business" , required=True)
    company_name = fields.Char(string= "Company Name" , required=True)
    company_address = fields.Char(string= "Company Address" , required=True)
    cnic_front = fields.Binary(string="CNIC Front" , required=True)
    cnic_back = fields.Binary(string="CNIC Back" , required=True)
    security_cheque = fields.Binary(string="Security Cheque", required=True)
    customer_image = fields.Binary(string="Customer Image", required=True)
    region = fields.Char(String="Region")
    user_limit = fields.Float(string="User Limit")
    multi_document_lines = fields.One2many('multi.documents', 'partner_id', string='Multi Documents Lines')

    
    @api.model
    def create(self,vals):
        if vals.get('name', _('New')) == _('New'):
            vals['state'] = 'pending'
        res = super(Partner,self).create(vals)
        return res

    def approve_action(self):
        if self.product_type =="1":
            self['state'] = 'approve'
        elif self.product_type =="2":
            self['state'] = 'approve'
        # raise UserError('Hello')
    def reject_action(self):
        self['state'] = 'reject'
        # raise UserError('Hello')
class MultiDoc(models.Model):
    _name = "multi.documents"

    partner_id = fields.Many2one('res.partner')
    crm_id = fields.Many2one('crm.lead')

    uploader_name = fields.Char(string="Uploader Name")
    url = fields.Char(string="URL")
    description = fields.Char(string="Description")
    date = fields.Date(string="Date")