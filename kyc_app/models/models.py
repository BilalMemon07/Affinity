# -*- coding: utf-8 -*-
from odoo import models, fields, api, _
from odoo.exceptions import UserError

    
class Partner(models.Model):
    _inherit = 'res.partner'

    rejection_note = fields.Text(string ="Rejection Note")
    state = fields.Selection([('Idle', 'Idle'),('Revision_Required', 'Revision Required'), ('approve', 'Approved')],string='Status')
    # customer_code = fields.Char(string='Customer Code')
    product_type = fields.Selection([('1', 'Working Capital Lending'), ('2', 'Drive-Through Lending'),('3', 'Invoice Discounting'),('4', 'Tire Financing'),('5', 'Vehicle Leasing')], string='Product Type')
    gender = fields.Selection([('male', 'Male'), ('female', 'Female')], string='Gender')
    cnic_number = fields.Char(string='CNIC Number')
    father_name = fields.Char(string='Father Name')
    cnic_expiry_date = fields.Date(string='CNIC Expiry Date')
    date_of_birth = fields.Date(string='Date of Birth')
    birth_place = fields.Char(string='Birth Place')
    mailing_address = fields.Char(string='Mailing Address')
    permanent_address = fields.Char(string='Permanent Address')
    city_id = fields.Many2one('res.city',string='City')
    province_id = fields.Many2one('res.province',string='Provice')
    nature_of_business_id = fields.Many2one('res.nature',string='Nature of Business')
    requestor_income = fields.Float(string= "Requestor's Income (Monthly)")
    no_of_years = fields.Integer(string= "No of years in Business" )
    company_name = fields.Char(string= "Company Name" )
    company_address = fields.Char(string= "Company Address" )
    cnic_front = fields.Binary(string="CNIC Front" )
    cnic_front_name = fields.Binary(string="CNIC Front" )
    cnic_back = fields.Binary(string="CNIC Back" )
    cnic_back_name = fields.Binary(string="CNIC Back" )
    security_cheque = fields.Binary(string="Security Cheque")
    customer_image = fields.Binary(string="Customer Image")
    region = fields.Many2one('res.region', string='Region')    
    user_limit = fields.Float(string="User Limit")
    crm_id = fields.Many2one("crm.lead", string="CRM")
    multi_document_lines = fields.One2many('multi.documents', 'partner_id', string='Multi Documents Lines')


    # invoice discounting fields
    borrowers_requested_limit = fields.Float(string= "Borrower's Requested Limit" )
    business_recommended_limit = fields.Float(string= "Business Recommended Limit" )
    recommeded_interest_rate_per_month = fields.Float(string= "Recommeded Interest Rate per month" )
    approved_limit  = fields.Float(string= "Approved Limit" )
    approved_interest_rate  = fields.Float(string= "Approved Interest Rate" )
    default_under_writing_authority  = fields.Selection([('Meezan Bank Limited', 'Meezan Bank Limited'), ('Bank Al Habib', 'Bank Al Habib'),('Trukkr Financial Services', 'Trukkr Financial Services')], string= "Default Under Writing Authority" )
    assosiated_corporate  = fields.Char(string= "Assosiated Corporate" )
    # Working Capital Fields

    borrowers_requested_limit_wl = fields.Float(string= "Borrower's Requested Limit" )
    business_recommended_limit_wl = fields.Float(string= "Business Recommended Limit" )
    recommeded_interest_rate_per_month_wl = fields.Float(string= "Recommeded Interest Rate per month" )
    approved_limit_wl = fields.Float(string= "Approved Limit" )
    approved_interest_rate_wl = fields.Float(string= "Approved Interest Rate" )
    # Drive Throught Fields 
    borrowers_requested_limit_dtl = fields.Float(string= "Borrower's Requested Limit" )
    business_recommended_limit_dtl = fields.Float(string= "Business Recommended Limit" )
    recommeded_interest_rate_per_month_dtl = fields.Float(string= "Recommeded Interest Rate per month" )
    approved_limit_dtl = fields.Float(string= "Approved Limit" )
    approved_interest_rate_dtl = fields.Float(string= "Approved Interest Rate" )
    applicable_interest_rate = fields.Float(string= "Applicable Interest Rate" )

    # confirm appreove stages fields 
    approve_for_DTL = fields.Boolean(string = "Approve For DTL")
    approve_for_BL = fields.Boolean(string = "Approve For BL")
    approve_for_ID = fields.Boolean(string = "Approve For ID")
    
    status_of_DTL = fields.Selection([('Idle', 'Idle'),('Revision_Required', 'Revision Required'), ('approve', 'Approved')], string = "Status of DTL")
    status_of_BL = fields.Selection([('Idle', 'Idle'),('Revision_Required', 'Revision Required'), ('approve', 'Approved')], string = "Status of BL")
    status_of_ID = fields.Selection([('Idle', 'Idle'),('Revision_Required', 'Revision Required'), ('approve', 'Approved')], string = "Status of ID")
    
    key_personnel_details_lines = fields.One2many('key.personnel.details', 'customer_id', string='Key Personnel Details Lines')
    authorized_signatory_details_lines = fields.One2many('authorized.signatory.details', 'customer_id', string='Authorized Signatory Details Lines')

# confirm approve stages fields


    @api.model
    def create(self,vals):
        # if vals.get('name', _('New')) == _('New'):
        # vals['state'] = 'Idle'
        vals['status_of_DTL'] = 'Idle'
        vals['status_of_BL'] = 'Idle'
        vals['status_of_ID'] = 'Idle'
        res = super(Partner,self).create(vals)
        return res

    def approve_action(self):
        if self.product_type =="1":
            self['state'] = 'approve'
        elif self.product_type =="2":
            self['state'] = 'approve'
        # raise UserError('Hello')
    def revision_action(self):
        self['state'] = 'Revision_Required'

class MultiDoc(models.Model):
    _name = "multi.documents"

    partner_id = fields.Many2one('res.partner')

    uploader_name = fields.Char(string="Document Name")
    url = fields.Binary(string="Document")
    url_name = fields.Char(string="Document")
    description = fields.Char(string="Description")
    date = fields.Date(string="Date")


