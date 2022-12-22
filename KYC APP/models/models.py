# -*- coding: utf-8 -*-
from odoo import models, fields, api, _
from odoo.exceptions import UserError

    
class Partner(models.Model):
    _inherit = 'res.partner'

    customer_name = fields.Char(string='Customer Name', required=True)
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
    

