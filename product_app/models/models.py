# -*- coding: utf-8 -*-
from odoo import models, fields, api, _
from odoo.exceptions import UserError
from datetime import datetime
    


class Leads(models.Model):
    _inherit = 'crm.lead'
    
    commission=fields.Float(string="Interest Rate")
    amount=fields.Float(string="Amount")
    invoice_status = fields.Selection([
        ('to_invoice', 'To Invoice'),
        ], string='Invoice Status', store=True)
    state = fields.Selection([('pending', 'Pending'), ('approve', 'Approved'), ('reject', 'Reject')], string='Status', default='pending')
    product_type = fields.Selection([('1', 'Working capital Financing'), ('2', 'Drive Throught Lending'),('3', 'Invoice Discounting')], string='Product Type', required=True) 
    limit_request = fields.Float(string= "limit Request") #for (b)
    requested_amount = fields.Float(string= "Requested Amount") #for (b/d)
    instrument_number = fields.Char(string= "Instrument Number") #for (b/d)
    instrument_number = fields.Char(string= "Instrument Number") #for (b/d)
    facility_request_date = fields.Date(string= "Facility Request date") #for (b/d/i)
    instrument_due_date = fields.Date(string= "Facility due date") #for (b/d/i)
    attachment = fields.Binary(string= "Attachment") #for (b/d)
    attachment_name = fields.Char(string= "Attachment") #for (b/d)

    interest_rate = fields.Float(string= "Interest Rate") 

    # for invoice
    select_party = fields.Char(string="Select Party (coporate)") #for (i)
    invoice_amount = fields.Float(string="Invoice Amount") #for (i)
    tag_trip = fields.Float(string="Tag Trip") #for (i)
    invoice_type = fields.Selection([('1', 'Transportation Invoice'), ('2', 'Good Invoice')], string='Invoice Type') #for (i)
    description = fields.Text(string="escription") #for (i)
    invoice_attachment = fields.Binary(string= "Upload Invoice") #for (i)
    invoice_attachment_name = fields.Char(string= "Upload Invoice") #for (i)

    # related_stage_name = fields.Related('stage_id','name', type="char",string="stage")
    related_stage_name = fields.Char(string='stage', related='stage_id.name')
    related_team_id = fields.Char(string='Team', related='team_id.name')


    # for Business Team 
    bank_attachment = fields.Binary(string= "Bank Attactment")
    bank_attachment_name = fields.Char(string= "Bank Attactment")
    trip_data = fields.Binary(string= "Trip Data")
    trip_data_name = fields.Char(string= "Trip Data")
    ownership_doc = fields.Binary(string= "Truck Ownership")
    ownership_doc_name = fields.Char(string= "Truck Ownership")
    # for Business Team & Risk & Compliance

    kyc_check = fields.Boolean(string = 'Kyc check with NADRA')
    bureau_check = fields.Boolean(string = 'Credit Bureau Check')
    risk_score = fields.Float(string="Risk Score Calculation")
    assign_limit = fields.Float(string="Assign Limit")

    # for Business Team & Risk & Compliance & Management

    priority = fields.Selection([('0', 'Normal'),('1', 'Good'),('2', 'Very Good'),('3', 'Excellent')], string="Priority", default='0')
    Note = fields.Text(string="Appreciation",)
    rejection_note = fields.Text(string="Rejection Note")
    crm_count = fields.Integer(string='Invoice', compute='get_crm_count')

    # for Rick Score calculation Fields

    company_structure = fields.Selection([('5_sole_owner_partnership_10', 'Sole Owner/Partnership'),('10_registered_entry_10', 'Registered Entry')], string="Company Structure")
    business_type = fields.Selection([('5_LTV_5', 'LTV'),('10_HTV_5', 'HTV'),('8_LTV_and_HTV_5', 'LTV And HTV')], string="Business Type")
    monthly_revenue = fields.Selection([('3_10_Mn_20', '10 Mn'),('6_25_Mn_20', '25 Mn'),('8_25_Mn_20', '50 Mn'),('10_Over_50_Mn_20', 'Over 50 Mn')], string="Monthly Revenue/size of business")
    no_of_years  = fields.Selection([('3_0_2_years_20', '0-2 Years'),('6_2_6_years_20', '2-6 Years'),('8_6_10_years_20', '6-10 Years'),('10_Over_10_Years_20', 'Over 10 Years')], string="No of years in business")
    customer_type  = fields.Selection([('5_Open_Market_10', 'Open Market'),('5_Coporates_and_Open_Market_10', 'Open Market And Coporates'),('10_coporates_10', 'Coporates')], string="Which Type Of Customers Deal With")
    pep  = fields.Selection([('10_no_5', 'No'),('0_yes_5', 'Yes')], string="PEP")
    availability_of_bank_statement  = fields.Selection([('0_no_10', 'No'),('10_yes_10', 'Yes')], string="Availability Of Bank Statement")
    repayment_history  = fields.Selection([('10_no_overdue_15', 'No Overdue'),('8_5_days_over_due_15', '5 Days Overdue'),('6_15_days_overdue_15', '15 Days Overdue'),('4_15_30_days_overdue_15', '15-30 Days Overdue'),('2_30_Days_Overdue_15', '30 Days Overdue'),('0_no_history_15', 'No History')], string="Repayment History")
    truck_ownership  = fields.Selection([('0_no_trucks_5', 'No Trucks'),('3_1_3_trucks_5', '1-3 Trucks'),('6_4_10_trucks_5', '4-10 Trucks'),('8_11_20_trucks_5', '11-20 Trucks'),('10_over_20_trucks_5', 'Over 20 Trucks'),], string="Truck/Fleet Ownership")
    
    # score fields 

    company_score = fields.Float(String =  "Company Score" ,readonly = True)
    business_score = fields.Float(String =  "Business Score" ,readonly = True)
    revenue_score = fields.Float(String =  "Revenue Score" ,readonly = True)
    years_score = fields.Float(String =  "Years Score" ,readonly = True)
    customer_score = fields.Float(String =  "Customer Score" ,readonly = True)
    pep_score = fields.Float(String =  "PEP Score" ,readonly = True)
    statement_score = fields.Float(string = "Statement Score" ,readonly = True)
    repayment_score = fields.Float(string = "Repayment Score" ,readonly = True)
    truck_score = fields.Float(string = "Truck Score" ,readonly = True)

    # weight fields

    company_weight = fields.Float(String =  "Company weight"  ,readonly = True)
    business_weight = fields.Float(String =  "Business weight" ,readonly = True)
    revenue_weight = fields.Float(String =  "Revenue weight" ,readonly = True)
    years_weight = fields.Float(String =  "Years weight" ,readonly = True)
    customer_weight = fields.Float(String =  "Customer weight" ,readonly = True)
    pep_weight = fields.Float(String =  "PEP weight" ,readonly = True)
    statement_weight = fields.Float(string = "Statement weight" ,readonly = True)
    repayment_weight = fields.Float(string = "Repayment weight" ,readonly = True)
    truck_weight = fields.Float(string = "Truck weight" ,readonly = True)
    total_weight = fields.Float(string = "total weight" ,readonly = True)

    # Weighted Score Fields  

    company_weighted = fields.Float(String =  "Company weighted"  ,readonly = True)
    business_weighted = fields.Float(String =  "Business weighted" ,readonly = True)
    revenue_weighted = fields.Float(String =  "Revenue weighted" ,readonly = True)
    years_weighted = fields.Float(String =  "Years weighted" ,readonly = True)
    customer_weighted = fields.Float(String =  "Customer weighted" ,readonly = True)
    pep_weighted = fields.Float(String =  "PEP weighted" ,readonly = True)
    statement_weighted = fields.Float(string = "Statement weighted" ,readonly = True)
    repayment_weighted = fields.Float(string = "Repayment weighted" ,readonly = True)
    truck_weighted = fields.Float(string = "Truck weighted" ,readonly = True)
    total_weighted = fields.Float(string = "Total weighted Score" ,readonly = True)

    # Extra Fields 
    risk_level = fields.Char(string = "Risk Level" , readonly = True)
    invoice_id = fields.Many2one('account.move', string="Invoice")
    disbursment_id = fields.Many2one('account.disbursement', string="Disbursment")
    invoice_state = fields.Selection( string='Invoice State', related='invoice_id.state') 
    disbursement_state = fields.Selection( string='Disbursment State', related='disbursment_id.state')
    multi_document_lines = fields.One2many('multi.documents.crm', 'crm_id', string='Multi Documents Lines')




    # **************************** Fields For Customer Pipeline **************************************
    #              ****************General Information Fields ********************************

    customer_name = fields.Char(string='Customer/CEO Name (As per CNIC)', )
    gender = fields.Selection([('male', 'Male'), ('female', 'Female')], string='Gender', )
    cnic_number = fields.Char(string='CNIC Number')
    father_name = fields.Char(string='Father Name')
    cnic_expiry_date = fields.Date(string='CNIC Expiry Date')
    date_of_birth = fields.Date(string='Date of Birth')
    birth_place = fields.Char(string='Birth Place')
    mailing_address = fields.Char(string='Mailing Address')
    permanent_address = fields.Char(string='Permanent Address')
    city = fields.Char(string='City')
    province = fields.Char(string='Provice')
    ntn_number = fields.Char(string='NTN Number')
    ownership_struture = fields.Selection([('sole_owner', 'Sole Owner'), ('partnership', 'partnership'),('registered_company', 'Registered Company')], string='Ownership Structure' )
    business_development_officer = fields.Selection([('Jawwad', 'Jawwad'), ('Bilal', 'Bilal'),('Hasan', 'Hasan'),('kasra', 'kasra')], string='Business Development Officer' )
    supervising_manager = fields.Selection([('Jawwad', 'Jawwad'), ('Bilal', 'Bilal'),('Hasan', 'Hasan'),('kasra', 'kasra')], string='Supervising Manager' )
    
    instrument_lines = fields.One2many('instrument', 'crm_id', string='Instrument Lines')

    # #              ****************Business Information Fields ********************************

    nature_of_business = fields.Char(string='Nature of Business')
    requestor_income = fields.Float(string= "Requestor's Income (Monthly)")
    no_of_years = fields.Integer(string= "No of years in Business" )
    company_name = fields.Char(string= "Company Name" )
    company_address = fields.Char(string= "Company Address" )
    other_sources_of_income = fields.Char(string= "Other sources of income" )
    
    # #              ****************Business Information Fields ********************************

    key_personnel_details_lines = fields.One2many('key.personnel.details', 'crm_id', string='Key Personnel Details Lines')
    authorized_signatory_details_lines = fields.One2many('authorized.signatory.details', 'crm_id', string='Authorized Signatory Details Lines')
    details_of_director_share_holder_lines = fields.One2many('details.of.director.share.holder', 'crm_id', string='Details Of Director / Share Holder Lines')

    
    
    # #              ****************Invoice Discounting Loan Fields ********************************
    
    requested_loan_amount = fields.Float(string="Requested Loan Amount")
    approved_loan_amount = fields.Float(string="Approved Loan Amount")
    applicable_interest_rate = fields.Float(string="Applicable Interest Rate")
    approved_interest_rate = fields.Float(string="Approved Interest Rate")
    approved_limit = fields.Float(string="Approved Limit")
    principal_outstanding = fields.Float(string="Principal Outstanding")
    interest_outstanding = fields.Float(string="Interest Outstanding")
    total_receivable_amount = fields.Float(string="Total Receivable Amount")
    tenor = fields.Integer(string="Tenor")
    invoice_numbr = fields.Char(string="Invoice Number")
    attach_invoices = fields.Binary(string="Attach Invoices")
    attach_invoices_name = fields.Char(string="Attach Invoices")
    No_of_blts = fields.Float(string="No. of BLTs")
    underwriting_authority = fields.Selection([('Meezan Bank Limited', 'Meezan Bank Limited'), ('Bank Al Habib', 'Bank Al Habib'),('Trukkr Financial Services', 'Trukkr Financial Services')],string="Underwriting authority")
    Attach_BLTs = fields.Binary(string="Attach BLTs")
    Attach_BLTs_name = fields.Char(string="Attach BLTs")
    
    
    @api.onchange("product_type")
    def check_customer_approve(self):
        if self.partner_id:
            if self.product_type:
                if self.product_type == "1" and self.partner_id.approve_for_BL == False:
                    pass
                elif self.product_type == "2" and self.partner_id.approve_for_DTL == False:
                    pass
                elif self.product_type == "3" and self.partner_id.approve_for_ID == False:
                    pass
                else:
                    self._fields['product_type'].string
                    raise UserError(str(dict(self._fields['product_type'].selection).get(self.product_type)) + " is already approve please select another")

    @api.onchange("partner_id")
    def partner_details(self):
        if self.partner_id:
            if self.product_type == 3:
                self['applicable_interest_rate'] = self.partner_id.approved_interest_rate
                self['approved_interest_rate'] = self.partner_id.approved_interest_rate
                self['approved_limit'] = self.partner_id.approved_limit
                self['underwriting_authority'] = self.partner_id.default_under_writing_authority
            elif self.product_type == 2:
                self['applicable_interest_rate'] = self.partner_id.approved_interest_rate_dtl
                self['approved_interest_rate'] = self.partner_id.approved_interest_rate_tdl
                self['approved_limit'] = self.partner_id.approved_limit_dtl
                self['underwriting_authority'] = self.partner_id.default_under_writing_authority_dtl
            elif self.product_type == 1:
                self['applicable_interest_rate'] = self.partner_id.approved_interest_rate_wl
                self['approved_interest_rate'] = self.partner_id.approved_interest_rate_wl
                self['approved_limit'] = self.partner_id.approved_limit_wl
                self['underwriting_authority'] = self.partner_id.default_under_writing_authority_wl

            self['customer_name'] = self.partner_id.name
            self['gender'] = self.partner_id.gender
            self['cnic_number'] = self.partner_id.cnic_number
            self['father_name'] = self.partner_id.father_name
            self['cnic_expiry_date'] = self.partner_id.cnic_expiry_date
            self['date_of_birth'] = self.partner_id.date_of_birth
            self['birth_place'] = self.partner_id.birth_place
            self['mailing_address'] = self.partner_id.mailing_address
            self['permanent_address'] = self.partner_id.permanent_address
            self['city'] = self.partner_id.city
            self['province'] = self.partner_id.province
            self['nature_of_business'] = self.partner_id.nature_of_business
            self['requestor_income'] = self.partner_id.requestor_income
            self['no_of_years'] = self.partner_id.no_of_years
            self['company_name'] = self.partner_id.company_name
            self['company_address'] = self.partner_id.company_address




    def get_crm_count(self):
        count = self.env['account.move'].search_count([('crm_id', '=', self.id)])
        self.crm_count = count  
    @api.onchange("instrument_due_date","facility_request_date")
    def calculate_tenor(self):
        if self.instrument_due_date and self.facility_request_date:
            tenor = self['instrument_due_date'] - self['facility_request_date']
            final_date = str(tenor).split(" ")[0]
            self['tenor'] = float(final_date) 

    @api.onchange("approved_loan_amount","applicable_interest_rate","tenor")
    def calculate_total_receivable(self):
        if self.tenor:
            connission = self['approved_loan_amount'] * (self['applicable_interest_rate'] / 100)
            total = connission * self['tenor']
            self['total_receivable_amount'] = total


    def open_patient_appointment(self):
        return {
            'name': 'Invoice',
            'domain': [('crm_id', '=', self.id)],
            'view_type': 'form',
            'res_model': 'account.move',
            'view_id': False,
            'view_mode': 'tree,form',
            'type': 'ir.actions.act_window'
        }

    @api.model
    def create(self,vals):
        if vals.get('name', _('New')) == _('New'):
            vals['state']='pending'
        res = super(Leads,self).create(vals)
        return res


    # def approve_action(self):
    #     if self.team_id.id == 1:
    #         # if self.product_type == '1' or self.product_type == '3':
    #         crm_lead = self.env['crm.lead'].search([('partner_id','=', self.partner_id.id),('team_id','=', 5)])
    #         # raise UserError(crm_lead)
            
    #         if self.product_type == '1':
    #             if crm_lead.stage_id.id == 7:
    #                 self['stage_id'] = 4
    #                 self['state'] = 'approve'
    #         elif self.product_type == '2':
    #             if crm_lead.stage_id.id == 7:
    #                 self['stage_id'] = 5
    #                 self['state'] = 'approve'
                
    #         elif self.product_type == '3':
    #             if crm_lead.stage_id.id == 7:
    #                 self['stage_id'] = 4
    #                 self['state'] = 'approve'
    #                 # self['state'] ='pending'
    #         # else:
    #         #     self['state'] = 'approve'
    #         #     self['stage_id'] = 5
    #     elif self.team_id.id == 5:
    #         # raise UserError(self.team_id.id)
    #         if self.stage_id.id == 6: 
    #             self['state'] = 'approve'
    #             self['stage_id'] = 7
    #             self['state'] ='pending'
    #         elif self.stage_id.id == 7:
    #             self['state'] = 'approve'
    #             # raise UserError("Hello")
    #             if self.state == "approve":
    #                 if self.team_id.id == 5:
    #                     if self.stage_id.id == 7: 
    #                         obj = {
    #                         'name': self.name,
    #                         }
    #                         customer = self.env['res.partner'].create(obj)
    #                         if customer:
    #                             self['partner_id'] = customer.id
    
    def approve_action(self):
        if self.team_id.id == 1:
            if self.product_type == '1' or self.product_type == '3':
                if self.product_type == '1': 
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
                        self['stage_id'] = 4
                if self.product_type == '3':  
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
                        self['stage_id'] = 8
                    # self['state'] ='pending'
            else:
                self['state'] = 'approve'
                self['stage_id'] = 5
        elif self.team_id.id == 5:
            if self.product_type == '1' or self.product_type == '3':
                if self.stage_id.id == 11: 
                    self['state'] = 'approve'
                    self['stage_id'] = 12
                    self['state'] ='pending'
                elif self.stage_id.id == 12: 
                    self['state'] = 'approve'
                    self['stage_id'] = 13
                    self['state'] ='pending'
                elif self.stage_id.id == 13:
                    if self.product_type == '1':
                        self['stage_id'] = 6
                        self['state'] = 'approve'
                    elif self.product_type == "3":
                        self['stage_id'] = 10
                        self['state'] = 'approve'                             
                    # raise UserError("Hello")
            else:
                self['state'] = 'approve'
                self['stage_id'] = 7

            if not self['partner_id']:
                if self.state == "approve":
                    if self.stage_id.id == 10 or self.stage_id.id == 6 or self.stage_id.id == 7: 
                        obj = {
                        'name': self.customer_name,
                        'gender': self.gender,
                        'cnic_number':self.cnic_number,
                        'father_name':self.father_name,
                        'cnic_expiry_date':self.cnic_expiry_date,
                        'date_of_birth':self.date_of_birth,
                        'birth_place':self.birth_place,
                        'mailing_address':self.mailing_address,
                        'permanent_address':self.permanent_address,
                        'city':self.city,
                        'province':self.province,
                        # company Information
                        'nature_of_business':self.nature_of_business,
                        'requestor_income':self.requestor_income,
                        'no_of_years':self.no_of_years,
                        'company_name':self.company_name,
                        'company_address':self.company_address,
                        }
                        customer = self.env['res.partner'].create(obj)
                        if customer:
                            self['partner_id'] = customer.id
            if self.stage_id.id == 6:
                self['partner_id']['approve_for_BL'] = True
            elif self.stage_id.id == 7:
                self['partner_id']['approve_for_DTL'] = True
            elif self.stage_id.id == 10:
                self['partner_id']['approve_for_ID'] = True

    def risk_calculation(self):
        total_weight = 0
        total_weighted = 0
        if self.company_structure:
            self['company_score'] = self.company_structure.split('_')[0] 
            self['company_weight'] = self.company_structure.split('_')[-1]
            total_weight += self['company_weight']
            self['company_weighted'] = (self['company_score'] * self['company_weight']) / 100
            total_weighted += self['company_weighted']
        if self.business_type:
            self['business_score'] = self.business_type.split('_')[0] 
            self['business_weight'] = self.business_type.split('_')[-1]
            total_weight += self['business_weight']
            self['business_weighted'] = (self['business_score'] * self['business_weight']) / 100
            total_weighted += self['business_weighted']
        if self.monthly_revenue:
            self['revenue_score'] = self.monthly_revenue.split('_')[0] 
            self['revenue_weight'] = self.monthly_revenue.split('_')[-1]
            total_weight += self['revenue_weight']
            self['revenue_weighted'] = (self['revenue_score'] * self['revenue_weight']) / 100
            total_weighted += self['revenue_weighted']
        if self.no_of_years:
            self['years_score'] = self.no_of_years.split('_')[0] 
            self['years_weight'] = self.no_of_years.split('_')[-1]
            total_weight += self['years_weight']
            self['years_weighted'] = (self['years_score'] * self['years_weight']) / 100
            total_weighted += self['years_weighted']
        if self.customer_type:
            self['customer_score'] = self.customer_type.split('_')[0] 
            self['customer_weight'] = self.customer_type.split('_')[-1]
            total_weight += self['customer_weight']
            self['customer_weighted'] = (self['customer_score'] * self['customer_weight']) / 100
            total_weighted += self['customer_weighted']
        if self.pep:
            self['pep_score'] = self.pep.split('_')[0] 
            self['pep_weight'] = self.pep.split('_')[-1]
            total_weight += self['pep_weight']
            self['pep_weighted'] = (self['pep_score'] * self['pep_weight']) / 100
            total_weighted += self['pep_weighted']
        if self.availability_of_bank_statement:
            self['statement_score'] = self.availability_of_bank_statement.split('_')[0] 
            self['statement_weight'] = self.availability_of_bank_statement.split('_')[-1]
            total_weight += self['statement_weight']
            self['statement_weighted'] = (self['statement_score'] * self['statement_weight']) / 100
            total_weighted += self['statement_weighted']
        
        if self.repayment_history:
            self['repayment_score'] = self.repayment_history.split('_')[0] 
            self['repayment_weight'] = self.repayment_history.split('_')[-1]
            total_weight += self['repayment_weight']
            self['repayment_weighted'] = (self['repayment_score'] * self['repayment_weight']) / 100
            total_weighted += self['repayment_weighted']
        if self.truck_ownership:
            self['truck_score'] = self.truck_ownership.split('_')[0] 
            self['truck_weight'] = self.truck_ownership.split('_')[-1]
            total_weight += self['truck_weight']
            self['truck_weighted'] = (self['truck_score'] * self['truck_weight']) / 100
            total_weighted += self['truck_weighted']
        
        
        self['total_weight'] = total_weight 
        self['total_weighted'] = total_weighted 
        if self.total_weighted < 4:
            self['risk_level'] = "High Risk"
        elif self.total_weighted > 4 and self.total_weighted < 7:
            self['risk_level'] = "Mid Risk"
        elif self.total_weighted > 7:
            self['risk_level'] = "Low Risk"

    def reject_action(self):
        if self.team_id.id == 1:
            if self.stage_id.id == 1:
                if self.rejection_note:
                    self['state']='reject'
                    self['description'] =  ' ● '+  str(self.rejection_note) + ' ' +'('+ str(self.related_stage_name) + ')' + '\n' 
                    self['rejection_note'] = False
                else:
                    raise UserError('Please Enter The Rejection Note')
            elif self.stage_id.id == 2:
                self['company_structure'] = False
                self['business_type'] = False
                self['monthly_revenue'] = False
                self['no_of_years'] = False
                self['customer_type'] = False
                self['pep'] = False
                self['availability_of_bank_statement'] = False
                self['repayment_history'] = False
                self['truck_ownership'] = False
                self['company_score'] = 0
                self['business_score'] = 0
                self['revenue_score'] = 0
                self['years_score'] = 0
                self['customer_score'] = 0
                self['pep_score'] = 0
                self['statement_score'] = 0
                self['repayment_score'] = 0
                self['truck_score'] = 0
                self['company_weight'] = 0
                self['business_weight'] = 0
                self['revenue_weight'] = 0
                self['years_weight'] = 0
                self['customer_weight'] = 0
                self['pep_weight'] = 0
                self['statement_weight'] = 0
                self['repayment_weight'] = 0
                self['truck_weight'] = 0
                self['company_weighted'] = 0
                self['business_weighted'] = 0
                self['revenue_weighted'] = 0
                self['years_weighted'] = 0
                self['customer_weighted'] = 0
                self['pep_weighted'] = 0
                self['statement_weighted'] = 0
                self['repayment_weighted'] = 0
                self['truck_weighted'] = 0
                self['total_weight'] = 0
                self['total_weighted'] = 0
                if self.rejection_note:
                    self['state']='reject'
                    self['description'] =  str(self.description) + " " +'● '+  str(self.rejection_note) + ' ' +'('+ str(self.related_stage_name) + ')' + '\n'  
                    self['rejection_note'] = False
                    self['stage_id'] = 1
                    self['state'] ='pending'
                else:
                    raise UserError('Please Enter The Rejection Note')
            elif self.stage_id.id == 3:
                if self.rejection_note:
                    self['state']='reject'
                    self['description'] =  str(self.description) + " " +' ● '+  str(self.rejection_note) + ' ' + '('+ str(self.related_stage_name) + ')' + '\n '
                    self['rejection_note'] = False
                    self['stage_id'] = 2
                    self['state'] ='pending'
                else:
                    raise UserError('Please Enter The Rejection Note')
            elif self.stage_id.id == 4:
                if self.rejection_note:
                    self['state']='reject'
                    self['description'] =   str(self.description) + " " +' ● '+  str(self.rejection_note) + ' ' + '('+ str(self.related_stage_name) + ')' + '\n '
                    self['rejection_note'] = False
                    self['stage_id'] = 1
                    self['state'] ='pending'
                else:
                    raise UserError('Please Enter The Rejection Note')
            elif self.stage_id.id == 5:
                if self.rejection_note:
                    self['state']='reject'
                    self['description'] =   str(self.description) + " " +' ● '+  str(self.rejection_note) + ' ' + '('+ str(self.related_stage_name) + ')' + '\n '
                    self['rejection_note'] = False
                    self['stage_id'] = 1
                    self['state'] ='pending'
            elif self.stage_id.id == 8:
                if self.rejection_note:
                    self['state']='reject'
                    self['description'] =   str(self.description) + " " +' ● '+  str(self.rejection_note) + ' ' + '('+ str(self.related_stage_name) + ')' + '\n '
                    self['rejection_note'] = False
                    self['stage_id'] = 3
                    self['state'] ='pending'
                else:
                    raise UserError('Please Enter The Rejection Note')
        
        
        # raise UserError("Helllo")
    # "Drive-Through Lending" "Working Capital Lending"
    @api.onchange('product_type','partner_id')
    def partner_id_domain_pur(self):
        if self.product_type == '1': 
            return {"domain": {'partner_id': [('state', '=', 'approve')]}}
        return {"domain": {'partner_id': []}}

    def action_create_invoice(self):
        lines = []
        interestlines = []
        product_id = 0
        if self.product_type == '1':
            product_id = 2
        elif self.product_type == '2':
            product_id = 1
        days = self.instrument_due_date - self.facility_request_date
        final_date = str(days).split(" ")[0]
        
        for rec in self:
            if (self.approved_loan_amount <= 0 and self.approved_interest_rate <= 0) or (self.approved_loan_amount <= 0 or self.approved_interest_rate <= 0):    
                raise UserError('Amount or Commission  less then equal to 0')
            else:
                inv = self.env['account.move'].search([('crm_id','=',rec.id)])
                if inv:
                    rec['invoice_status'] = False
                else:
                    commission_value = 0
                    income_account = self.env['account.account'].search([('code', '=', "3111001")])
                    # receivable_account = self.env['account.account'].search([('code', '=', "1121001")])
                    commission_account = self.env['account.account'].search([('code', '=', "4311002")])
                    commission_by_day = (self.approved_interest_rate / float(30.5)) * float(final_date)
                    commission_value = (self.approved_loan_amount / 100) * commission_by_day
                    lines.append((0,0,{
                        'product_id':product_id,
                        # 'account_id' : income_account.id,
                        'quantity':1,
                        'price_unit' : rec.approved_loan_amount
                    }))
                    lines.append((0,0,{
                        'product_id': 3,
                        # 'account_id' : income_account.id,
                        'quantity':1,
                        'price_unit' : commission_value
                    }))
                    interest_id = self.env['product.template'].search([('id','=',product_id)])
                    interestlines.append((0, 0,
                        {
                        'account_id': interest_id.interest_account_id.id,
                        'debit': commission_value,
                        'exclude_from_invoice_tab': True
                        }
                    ))
                    move = self.env['account.move'].with_context(check_move_validity=False).create({
                    'journal_id': 1,
                    'invoice_date': datetime.now(),
                    'invoice_date_due': rec.instrument_due_date,
                    'invoice_line_ids':lines,
                    'move_type':'out_invoice',
                    'partner_id' : rec.partner_id.id,
                    'crm_id': rec.id,
                    })
                    receivale_id = move.partner_id.property_account_receivable_id
                    for line in move.line_ids:
                        if line.account_id == receivale_id:
                            line['debit'] = line['debit'] - commission_value
                    # raise UserError(str(interestlines))
                    move.with_context(check_move_validity=False).write({
                        'line_ids':interestlines
                    })
                    self['invoice_id'] = move.id
                    self['invoice_state'] = move.state

                    # for line in move.line_ids:
                    #     if line.account_id == income_account:
                    #         line['credit'] = line.credit-commission_value
                    #         break
 
    
    
      # move.action_post()       

# class Partner(models.Model):
#     _inherit = 'res.partner'

#     is_bl_approve = fields.Boolean(string="Is Bl Approve")
#     is_dtl_approve = fields.Boolean(string="Is DTL Approve")
#     is_id_approve = fields.Boolean(string="Is ID Approve")

class InstrumentNumber(models.Model):
    _name = 'instrument'

    crm_id = fields.Many2one('crm.lead')
    instrument_number = fields.Char(string="Instrument Number")
    instrument_due_date = fields.Date(string="Due Date")
    instrument_amount = fields.Float(string="Instrument Amount")
    instrument_document = fields.Binary(string="Document")
    instrument_document_name = fields.Char(string="Document")

class AccountMove(models.Model):
    _inherit = 'account.move'

    crm_id = fields.Many2one('crm.lead' , string="CRM")
    disbursement_id = fields.Many2one('account.disbursement' , string="Disbursement")
    dis_count = fields.Integer(string='Disbursment', compute='get_crm_count')

    def action_register_payment_custom(self):
        ''' Open the account.payment.register wizard to pay the selected journal entries.
        :return: An action opening the account.payment.register wizard.
        '''
        return {
            'name': _('Register Payment'),
            'res_model': 'register.payment',
            'view_mode': 'form',
            'context': {
                'active_model': 'account.move',
                'active_ids': self.ids,
            },
            'target': 'new',
            'type': 'ir.actions.act_window',
        }

    def get_crm_count(self):
        count = self.env['account.disbursement'].search_count([('invoice_id', '=', self.id)])
        self.dis_count = count
    def open_disbursment(self):
        return {
            'name': 'Disbursement',
            'domain': [('invoice_id', '=', self.id)],
            'view_type': 'form',
            'res_model': 'account.disbursement',
            'view_id': False,
            'view_mode': 'tree,form',
            'type': 'ir.actions.act_window'
        }

    def disbursement_payment(self):
        for rec in self:
            if rec.state == 'posted':
                payment_obj = rec.env['account.disbursement']
                amount = 0
                account_id = False
                for line in self.invoice_line_ids:
                    if line.name == "Drive-Through Lending":
                        account_id = line.account_id
                        amount =line.price_subtotal
                    if line.name == "Working Capital Lending":
                        account_id = line.account_id
                        amount =line.price_subtotal
                # sale_order = rec.env['sale.order'].search([('name','=',rec.invoice_origin)])
                # delivery_order = rec.env['stock.picking'].search([('origin','=',sale_order.name)])
                # for dev_line in delivery_order:
                # if sale_order:
                    # if dev_line['x_studio_courier'] == "Courier":
                        # if dev_line['x_studio_payment_type'] == "Cash" or dev_line['x_studio_payment_type'] == False:
                journal = self.env['account.journal'].search([('id', '=', 7)])
                payment_obj.create({
                    'vendor_id': rec.partner_id.id,
                    # 'payment_type' : 'outbound',
                    # 'partner_type' : 'customer',
                    # 'destination_account_id' : 32,
                    'memo':rec.name,
                    'journal_id' : False,
                    'payment_method':"Manual",
                    'date':datetime.now() ,
                    # 'payment_method_line_id': 2,#journal.outbound_payment_method_line_ids[0].id,
                    'amount': amount,
                    'invoice_id' :self.id
                    })

                rec.write({
                    'state' : 'posted'
                })
                # if payment_obj:
                # crm_model = self.env['crm.lead'].search([('id','=', rec.crm_id.id)])
                # raise UserError(payment_obj.document_name)
                    # rec['disbursement_id'] = crm_model.idmutl
                    
                #     for line in payment_obj.move_id.line_ids:
                #         if line.account_id.id == 32:
                #             raise UserError(line.account_id.name)
                #             line['account_id'] = account_id 


class Disbursementmodels(models.Model):
    _name='account.disbursement'
    _description='Disbursement'
    # fields used in payment forms
    document_name=fields.Char(string="Name" , required=True, copy=False, readonly=True,
                           index=True, default=lambda self: _('New'))
    internal_transfer=fields.Boolean(string='Internal Transfer')
    payment_type=fields.Selection([('Send', 'Send'), ('Receive', 'Receive')],string='Payment Type',required=True,default='Receive')
    vendor_id=fields.Many2one('res.partner',string='Vendor')

    amount=fields.Float(string='Amount')
    date=fields.Datetime(string='Date')
    memo=fields.Char(string='Memo')
    journal_id=fields.Many2one('account.journal',string='Journal')
    invoice_id=fields.Many2one('account.move',string='Invoice')
    bank_vendor_id=fields.Many2one('res.partner.bank',string="Vendor Bank Account")
    payment_method=fields.Selection([('Manual','Manual'),('Checks','Checks')],string="Payment Method",required=True)

    state=fields.Selection([('draft','Draft'),('post','Posted'),('cancel','cancelled')],string="Status")

    journal_count = fields.Integer(string='Entries', compute='get_crm_count')
    
    def get_crm_count(self):
        count = self.env['account.move'].search_count([('disbursement_id', '=', self.id)])
        self.journal_count = count

    def open_journal_entries(self):
        return {
            'name': 'Entries',
            'domain': [('disbursement_id', '=', self.id)],
            'view_type': 'form',
            'res_model': 'account.move',
            'view_id': False,
            'view_mode': 'tree,form',
            'type': 'ir.actions.act_window'
        }
    #configures record directory and sets it in name form
    def name_get(self):
        result = []
        for record in self:
            result.append((record.id,record.document_name))
        return result


    @api.model
    def create(self, values):
        values['state'] = 'draft'
        values['document_name'] = self.env['ir.sequence'].next_by_code('Dis_Seq') or _('New')
        return super(Disbursementmodels, self).create(values)

    def button_in_progress(self):
        # self.write({'state': "post"})
        for rec1 in self:  
            lines = []
            credit = 0
            invoice = self.env['account.move'].search([('name', '=', self.memo)])
            if invoice:
                for inv in invoice:
                    for invline in inv.invoice_line_ids:
                        if invline.name == "Drive-Through Lending" or invline.name == "Working Capital Lending":
                            
                            line = (0, 0, {
                                'account_id': rec1.journal_id.default_account_id.id,
                                'credit':invline.price_subtotal ,
                                'partner_id': rec1.vendor_id.id,
                            })
                            lines.append(line)
                            line = (0, 0, {
                                'account_id': invline.account_id.id,
                                'debit': invline.price_subtotal,
                                })
                            lines.append(line)
                        
                            jv =self.env['account.move'].create({
                            'journal_id': rec1.journal_id.id,
                            'date': rec1.date,
                            'line_ids': lines,
                            'ref': rec1.document_name,
                            'disbursement_id': rec1.id,
                            })
                            rec1.write({
                            'state': 'post',
                            })
                            jv.write({
                            'state': 'posted',
                            })

    def button_cancel(self):
        self.write({'state':'cancel'})
    
    def button_draft(self):
        self.write({'state' : 'draft'})
        # self.write({'state' : 'draft'})

# Subhan Product Model Work 
class ProductModel(models.Model):
    _inherit = 'product.template'

    interest_account_id = fields.Many2one('account.account', string="Interest Account Id")
class KeyPersonnalDetails(models.Model):
    _name = 'key.personnel.details'
    _description = 'Key Personnel Details'

    crm_id = fields.Many2one('crm.lead')
    full_name = fields.Char(string="Full Name",required=True)
    cnic = fields.Integer(string="Cnic#",required=True)
    designation =fields.Char(string="Designation",required=True)
    contact_no = fields.Integer(string = "Contact No",required=True)
    email_address = fields.Char(string = "Email Address")
    address = fields.Char(string = "Address")
class AuthorizedSignatoryDetails(models.Model):
    _name = 'authorized.signatory.details'
    _description = 'Authorized Signatory Details'

    crm_id = fields.Many2one('crm.lead')
    full_name = fields.Char(string="Full Name",required=True)
    cnic = fields.Integer(string="Cnic#",required=True)
    designation =fields.Char(string="Designation",required=True)
    contact_no = fields.Integer(string = "Contact No",required=True)
    email_address = fields.Char(string = "Email Address")
    address = fields.Char(string = "Address")
class DetailsOfDirectorShareHolder(models.Model):
    _name = 'details.of.director.share.holder'
    _description = 'Details of Director / Share Holder'

    crm_id = fields.Many2one('crm.lead')
    full_name = fields.Char(string="Full Name",required=True)
    cnic = fields.Integer(string="Cnic#",required=True)
    designation =fields.Char(string="Designation",required=True)
    contact_no = fields.Integer(string = "Contact No",required=True)
    email_address = fields.Char(string = "Email Address")
    address = fields.Char(string = "Address")

class MultiDocCRM(models.Model):
    _name = "multi.documents.crm"

    # partner_id = fields.Many2one('res.partner')
    crm_id = fields.Many2one('crm.lead')

    uploader_name = fields.Char(string="Uploader Name")
    url = fields.Char(string="URL")
    description = fields.Char(string="Description")
    date = fields.Date(string="Date")