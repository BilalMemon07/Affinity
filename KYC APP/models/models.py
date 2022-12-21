# -*- coding: utf-8 -*-
from odoo import models, fields, api, _
from odoo.exceptions import UserError

    
class Partner(models.Model):
    _inherit = 'res.partner'

    customer_name = fields.Char(string='Customer Name')
    gender = fields.Selection([('male', 'Male'), ('female', 'Female')], string='Gender')
    cnic_number = fields.Char(string='CNIC Number')
    father_name = fields.Char(string='Father Name')
    cnic_expiry_date = fields.Date(string='CNIC Expiry Date')
    date_of_birth = fields.Date(string='Date of Birth')
    birth_place = fields.Char(string='Birth Place')
    mailing_address = fields.Char(string='Mailing Address')
    permanent_address = fields.Char(string='Permanent Address')
    city = fields.Char(string='City')
    province = fields.Char(string='Provice')
    nature_of_business = fields.Char(string='Nature of Business')
    requestor_income = fields.Float(string= "Requestor's Income (Monthly)")
    no_of_years = fields.Integer(string= "No of years in Business")
    company_name = fields.Char(string= "Company Name")
    company_address = fields.Char(string= "Company Address")
    cnic_front = fields.Binary( help="Select image here",string="CNIC Front")
    cnic_back = fields.Binary( help="Select image here",string="CNIC Back")
    security_cheque = fields.Binary(help="Select image here",string="Security Cheque")
    

