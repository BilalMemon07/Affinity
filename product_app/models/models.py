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
    _no_of_years_  = fields.Selection([('3_0_2_years_20', '0-2 Years'),('6_2_6_years_20', '2-6 Years'),('8_6_10_years_20', '6-10 Years'),('10_Over_10_Years_20', 'Over 10 Years')], string="No of years in business")
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
    city_id = fields.Many2one('res.city',string='City')
    province_id = fields.Many2one('res.province',string='Provice')
    ntn_number = fields.Char(string='NTN Number')
    ownership_struture = fields.Selection([('sole_owner', 'Sole Owner'), ('partnership', 'partnership'),('registered_company', 'Registered Company')], string='Ownership Structure' )
    business_development_officer = fields.Many2one('hr.employee', string='Business Development Officer' )
    supervising_manager = fields.Many2one('hr.employee', string='Supervising Manager' )
    # new fields
    region = fields.Selection([('Karachi', 'Karachi'), ('Lahore', 'Lahore'),('Multan', 'Multan'),('Islamabad', 'Islamabad'),('Peshawar', 'Peshawar')], string='Region')
    
    instrument_lines = fields.One2many('instrument', 'crm_id', string='Instrument Lines')

    # #              ****************Business Information Fields ********************************

    nature_of_business_id = fields.Many2one('res.nature',string='Nature of Business')
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
    Corporate_Customer  = fields.Char(string="Corporate Customer")
    

    # Product Info Fields
    borrowers_requested_limit = fields.Float(string= "Borrower's Requested Limit" )
    business_recommended_limit = fields.Float(string= "Business Recommended Limit" )
    recommeded_interest_rate_per_month = fields.Float(string= "Recommeded Interest Rate per month" )
    approved_limit  = fields.Float(string= "Approved Limit" )
    approved_interest_rate  = fields.Float(string= "Approved Interest Rate" )
    default_under_writing_authority  = fields.Selection([('Meezan Bank Limited', 'Meezan Bank Limited'), ('Bank Al Habib', 'Bank Al Habib'),('Trukkr Financial Services', 'Trukkr Financial Services')], string= "Default Under Writing Authority" )
    assosiated_corporate  = fields.Char(string= "Assosiated Corporate" )
    
    # Document fields 
    # Working Capital
    B_S_l_6_m = fields.Binary(string="Bank Statement-last 6 months")
    name_B_S_l_6_m_name = fields.Char(string="Bank Statement-last 6 months")
    
    T_D_f_a_l_3_6_m = fields.Binary(string="Trip Data (for atleast last 3-6 months)")
    name_T_D_f_a_l_3_6_m_name = fields.Char(string="Trip Data (for atleast last 3-6 months)")
    
    A_l_p_u_b = fields.Binary(string="Any latest paid utility bill")
    name_A_l_p_u_b_name = fields.Char(string="Any latest paid utility bill")

    cnic_Front = fields.Binary(string="CNIC Front")
    name_cnic_Front_name = fields.Char(string="CNIC Front")
    
    CNIC_Back = fields.Binary(string="CNIC Back")
    name_CNIC_Back_name = fields.Char(string="CNIC Back")
    
    S_t_r_o_N = fields.Binary(string="Sales tax registration or NTN")
    name_S_t_r_o_N_name = fields.Char(string="Sales tax registration or NTN")

    S_P_D_o_b_l_h_f_R__B_a = fields.Binary(string="Sole Proprietorship Declaration on business letter head for Registered / Business address")
    name_S_P_D_o_b_l_h_f_R__B_a_name = fields.Char(string="Sole Proprietorship Declaration on business letter head for Registered / Business address")

    A_c_o_P_D_ = fields.Binary(string="Attested copy of ‘Partnership Deed’")
    name_A_c_o_P_D_name = fields.Char(string="Attested copy of ‘Partnership Deed’")
    
    P_o_i_d_a_t_p_a_a_s = fields.Binary(string="Photocopies of identity documents all the partners and authorized signatories.")
    name_P_o_i_d_a_t_p_a_a_s_name = fields.Char(string="Photocopies of identity documents all the partners and authorized signatories.")
    
    C_o_I = fields.Binary(string="Certificate of Incorporation")
    name_C_o_I_name = fields.Char(string="Certificate of Incorporation")
    
    R_o_B_o_D_f_o_o_a_s_t_p_a_t_o_a_o_t_a = fields.Binary(string="Resolution of Board of Directors for opening of account specifying the person(s) authorized to open and operate the account")
    name_R_o_B_o_D_f_o_o_a_s_t_p_a_t_o_a_o_t_a_name = fields.Char(string="Resolution of Board of Directors for opening of account specifying the person(s) authorized to open and operate the account")
    
    M_a_A_o_A = fields.Binary(string="Memorandum and Articles of Association")
    name_M_a_A_o_A_name = fields.Char(string="Memorandum and Articles of Association")
    
    C_c_o_L_F_A_F_B = fields.Binary(string="Certified copy of Latest ‘Form-A/Form-B’")
    name_C_c_o_L_F_A_F_B_name = fields.Char(string="Certified copy of Latest ‘Form-A/Form-B’")
    
    P_o_i_d_a_p_S_N_1_a_o_a_t_D_C = fields.Binary(string="Photocopies of identity documents as per Sr. No. 1 above of all the Directors/CEO")
    _1_name_P_o_i_d_a_p_S_N_1_a_o_a_t_D_C_name = fields.Char(string="Photocopies of identity documents as per Sr. No. 1 above of all the Directors/CEO.")
    
    P_o_i_d_a_p_S_N_1_a_o_t_b_o = fields.Binary(string="Photocopies of identity documents as per Sr. No. 1 above of the beneficial owners")
    _2_name_P_o_i_d_a_p_S_N_1_a_o_t_b_o_name = fields.Char(string="Photocopies of identity documents as per Sr. No. 1 above of the beneficial owners")
    
    F_A_F_C_w_i_a_a_F_2_i_a_i_c = fields.Binary(string="Form A / Form C whichever is applicable; and Form 29 in already incorporated companies")
    name_F_A_F_C_w_i_a_a_F_2_i_a_i_c_name = fields.Char(string="Form A / Form C whichever is applicable; and Form 29 in already incorporated companies")
    
    F_a = fields.Binary(string="Financing Agreement")
    name_F_a_name = fields.Char(string="Financing Agreement")
    
    # # Invoice Discounting 
    S_a_w_t_T_p = fields.Binary(string="Service agreement with the Third party")
    name_S_a_w_t_T_p_name = fields.Char(string="Service agreement with the Third party")

    S_I_H = fields.Binary(string="Sales Invoices (Historical)")
    name_S_I_H_name = fields.Char(string="Sales Invoices (Historical)")
    
    B_s_L_S_M_L = fields.Binary(string="Bank statements (Last Six Months – Latest)")
    name_B_s_L_S_M_L_name = fields.Char(string="Bank statements (Last Six Months – Latest)")

    S_T_R = fields.Binary(string="Sales Tax Returns")
    name_S_T_R_name = fields.Char(string="Sales Tax Returns")

    F_S = fields.Binary(string="Financial Statements")
    name_F_S_name = fields.Char(string="Financial Statements")

    P_o_i_d_a_p_S_N_1_a_o = fields.Binary(string="Photocopies of identity documents as per Sr. No. 1 above of")
    _3_name_P_o_i_d_a_p_S_N_1_a_o_name = fields.Char(string="Photocopies of identity documents as per Sr. No. 1 above of")
    
    a_t_D_C = fields.Binary(string="all the Directors/CEO.")
    name_a_t_D_C_name = fields.Char(string="all the Directors/CEO.")
    
    L_o_A_T_b_f_o_t_t_a_i_o_j = fields.Binary(string="Letter of Assignment (To be furnished once the trust account is open jointly)")
    name_L_o_A_T_b_f_o_t_t_a_i_o_j_name = fields.Char(string="Letter of Assignment (To be furnished once the trust account is open jointly)")
    
    P_L = fields.Binary(string="Promissory Letter")
    name_P_L_name = fields.Binary(string="Promissory Letter")
    
    I_D_A = fields.Binary(string="Invoice Discounting Agreement")
    name_I_D_A_name = fields.Char(string="Invoice Discounting Agreement")

    def compute_pipeline_to_partner(self):
        if self.team_id.id == 5:
            if self.product_type:
                partner = self.partner_id
                if self.partner_id:
                    if self.product_type == "3":
                        partner['borrowers_requested_limit'] = self.borrowers_requested_limit 
                        partner['business_recommended_limit'] = self.business_recommended_limit
                        partner['recommeded_interest_rate_per_month'] = self.recommeded_interest_rate_per_month
                        partner['approved_limit'] = self.approved_limit
                        partner['approved_interest_rate'] = self.approved_interest_rate
                        partner['default_under_writing_authority'] = self.default_under_writing_authority
                        partner['assosiated_corporate'] = self.assosiated_corporate
                    elif self.product_type == "1":
                        partner['borrowers_requested_limit_wl'] = self.borrowers_requested_limit 
                        partner['business_recommended_limit_wl'] = self.business_recommended_limit
                        partner['recommeded_interest_rate_per_month_wl'] = self.recommeded_interest_rate_per_month
                        partner['approved_limit_wl'] = self.approved_limit
                        partner['approved_interest_rate_wl'] = self.approved_interest_rate
                    elif self.product_type == "2":
                        partner['borrowers_requested_limit_dtl'] = self.borrowers_requested_limit 
                        partner['business_recommended_limit_dtl'] = self.business_recommended_limit
                        partner['recommeded_interest_rate_per_month_dtl'] = self.recommeded_interest_rate_per_month
                        partner['approved_limit_dtl'] = self.approved_limit
                        partner['approved_interest_rate_dtl'] = self.approved_interest_rate

    @api.onchange("product_type", "partner_id")
    def check_customer_approve(self):
        if self.team_id.id == 5:
            # if self.partner_id:
            #     partner_lead = self.env['crm.lead'].search([('partner_id','=',self.partner_id.id)])
            #     if partner_lead:
            #         # raise UserError(partner_lead)
            #         for rec in partner_lead:
            #             # if rec.partner_id.state == 'approve':
            #             #     rec['partner_id']['state'] = 'Revision_Required'
            if self.partner_id.approve_for_BL or self.partner_id.approve_for_DTL or self.partner_id.approve_for_ID:
                if self.product_type:
                    if self.product_type == "1" and self.partner_id.approve_for_BL == False:
                        self['partner_id']['status_of_BL'] = 'Revision_Required'
                        pass
                    elif self.product_type == "2" and self.partner_id.approve_for_DTL == False:
                        self['partner_id']['status_of_DTL'] = 'Revision_Required'
                        pass
                    elif self.product_type == "3" and self.partner_id.approve_for_ID == False:
                        self['partner_id']['status_of_ID'] = 'Revision_Required'
                        pass
                    else:
                        self._fields['product_type'].string
                        raise UserError(str(dict(self._fields['product_type'].selection).get(self.product_type)) + " is already approve please select another")

    @api.onchange("partner_id","product_type")
    def partner_details(self):
        if self.partner_id:
            if self.team_id.id == 1:
                if self.product_type == '3':
                    self['applicable_interest_rate'] = self.partner_id.approved_interest_rate
                    self['approved_interest_rate'] = self.partner_id.approved_interest_rate
                    self['approved_limit'] = self.partner_id.approved_limit
                    self['underwriting_authority'] = self.partner_id.default_under_writing_authority
                elif self.product_type == '2':
                    self['applicable_interest_rate'] = self.partner_id.applicable_interest_rate
                    self['approved_interest_rate'] = self.partner_id.approved_interest_rate_dtl
                    self['approved_limit'] = self.partner_id.approved_limit_dtl
                    # self['underwriting_authority'] = self.partner_id.default_under_writing_authority_dtl
                elif self.product_type == '1':
                    self['applicable_interest_rate'] = self.partner_id.approved_interest_rate_wl
                    self['approved_interest_rate'] = self.partner_id.approved_interest_rate_wl
                    self['approved_limit'] = self.partner_id.approved_limit_wl
                    # self['underwriting_authority'] = self.partner_id.default_under_writing_authority_wl

            self['customer_name'] = self.partner_id.name
            self['gender'] = self.partner_id.gender
            self['cnic_number'] = self.partner_id.cnic_number
            self['father_name'] = self.partner_id.father_name
            self['cnic_expiry_date'] = self.partner_id.cnic_expiry_date
            self['date_of_birth'] = self.partner_id.date_of_birth
            self['birth_place'] = self.partner_id.birth_place
            self['mailing_address'] = self.partner_id.mailing_address
            self['permanent_address'] = self.partner_id.permanent_address
            self['city_id'] = self.partner_id.city_id.id
            self['province_id'] = self.partner_id.province_id.id
            self['nature_of_business_id'] = self.partner_id.nature_of_business_id.id
            self['requestor_income'] = self.partner_id.requestor_income
            self['no_of_years'] = self.partner_id.no_of_years
            self['company_name'] = self.partner_id.company_name
            self['company_address'] = self.partner_id.company_address

            # if self['partner_id']['approve_for_BL'] or self['partner_id']['approve_for_DTL']  or self['partner_id']['approve_for_ID']:
            #     self['partner_id']['state'] = 'Revision_Required'
            # else:
            #     self['partner_id']['state'] = 'Idle'




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
            commission_by_day = (self.applicable_interest_rate / float(30)) * float(self['tenor'])
            commission_value = (self.approved_loan_amount / 100) * commission_by_day
            total = commission_value + self.approved_loan_amount 
            # raise UserError(commission_value)
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
    
    def approve_action(self):
        if self.team_id.id == 1:
            if self.product_type == '1' or self.product_type == '2':     
                if self.stage_id.id == 5: 
                    self['state'] = 'approve'
                    self['stage_id'] = 7
                    self['state'] ='pending'
                elif self.stage_id.id == 7:
                    self['state'] = 'approve'
                    self['stage_id'] = 9
                    self['state'] ='pending'
                elif self.stage_id.id == 9:
                    self['state'] = 'approve'
                    self['stage_id'] = 13
            if self.product_type == '3':  
                if self.stage_id.id == 5: 
                    self['state'] = 'approve'
                    self['stage_id'] = 7
                    self['state'] ='pending'
                elif self.stage_id.id == 7:
                    self['state'] = 'approve'
                    self['stage_id'] = 9
                    self['state'] ='pending'
                elif self.stage_id.id == 9:
                    self['state'] = 'approve'
                    self['stage_id'] = 11
                    self['state'] ='pending'
                elif self.stage_id.id == 11:
                    self['state'] = 'approve'
                    self['stage_id'] = 13
                # self['state'] ='pending'
        elif self.team_id.id == 5:
            if self.product_type == '1'  or self.product_type == '2' or self.product_type == '3':
                if self.stage_id.id == 6: 
                    self['state'] = 'approve'
                    self['stage_id'] = 8
                    self['state'] ='pending'
                elif self.stage_id.id == 8: 
                    self['state'] = 'approve'
                    self['stage_id'] = 10
                    self['state'] ='pending'
                elif self.stage_id.id == 10 and (self.product_type == '1' or  self.product_type == '2' ):
                    self['stage_id'] = 14
                    self['state'] = 'approve'
                    self['partner_id']['state'] = 'approve'
                elif self.stage_id.id == 10 and  self.product_type == '3':
                    self['state'] = 'approve'
                    self['stage_id'] = 12
                    self['state'] = 'pending'                             
                elif self.stage_id.id == 12:
                    self['stage_id'] = 14
                    self['state'] = 'approve'                             
                    self['partner_id']['state'] = 'approve'

                elif self.stage_id.id == 14:
                    self['state'] = 'approve'                             
                    self['partner_id']['state'] = 'approve'
                    # raise UserError("Hello")

            # else:
            #     self['state'] = 'approve'
            #     self['stage_id'] = 7
            #     self['partner_id']['state'] = 'approve'

            if self['partner_id']:
                if self.state == "approve":
                    self['partner_id']['state'] = 'approve'
                    if self.stage_id.id == 14: 
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
                        'city_id':self.city_id.id,
                        'province_id':self.province_id.id,
                        # company Information
                        'nature_of_business_id':self.nature_of_business_id.id,
                        'requestor_income':self.requestor_income,
                        'no_of_years':self.no_of_years,
                        'company_name':self.company_name,
                        'company_address':self.company_address,
                        }
                        partner = self.env['res.partner'].search([('id','=',self.partner_id.id)])
                        partner.write(obj)
                # else:
                #     self['partner_id']['state'] = 'Revision_Required'
            self.compute_pipeline_to_partner()
            if self.stage_id.id == 14 and self.product_type == '1' and self.state == "approve" :
                self['partner_id']['approve_for_BL'] = True
                self['partner_id']['status_of_BL'] = 'approve'

            elif self.stage_id.id == 14 and self.product_type == '2' and self.state == "approve":
                self['partner_id']['approve_for_DTL'] = True
                self['partner_id']['status_of_DTL'] = 'approve'
            elif self.stage_id.id == 14 and  self.product_type == '3' and self.state == "approve":
                self['partner_id']['approve_for_ID'] = True
                self['partner_id']['status_of_ID'] = 'approve'
                

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
        if self._no_of_years_:
            self['years_score'] = self._no_of_years_.split('_')[0] 
            self['years_weight'] = self._no_of_years_.split('_')[-1]
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
        if self.team_id.id == 5:
            if self.stage_id.id == 6:
                if self.rejection_note:
                    self['state']='reject'
                    self['description'] =  ' ● '+  str(self.rejection_note) + ' ' +'('+ str(self.related_stage_name) + ')' + '\n' 
                    self['rejection_note'] = False
                else:
                    raise UserError('Please Enter The Rejection Note')
            elif self.stage_id.id == 8:
                self['company_structure'] = False
                self['business_type'] = False
                self['monthly_revenue'] = False
                self['_no_of_years_'] = False
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
                    self['stage_id'] = 6
                    self['state'] ='pending'
                else:
                    raise UserError('Please Enter The Rejection Note')
            elif self.stage_id.id == 10:
                if self.rejection_note:
                    self['state']='reject'
                    self['description'] =  str(self.description) + " " +' ● '+  str(self.rejection_note) + ' ' + '('+ str(self.related_stage_name) + ')' + '\n '
                    self['rejection_note'] = False
                    self['stage_id'] = 8
                    self['state'] ='pending'
                else:
                    raise UserError('Please Enter The Rejection Note')
            elif self.stage_id.id == 12:
                if self.rejection_note:
                    self['state']='reject'
                    self['description'] =   str(self.description) + " " +' ● '+  str(self.rejection_note) + ' ' + '('+ str(self.related_stage_name) + ')' + '\n '
                    self['rejection_note'] = False
                    self['stage_id'] = 10
                    self['state'] ='pending'
                else:
                    raise UserError('Please Enter The Rejection Note')
            elif self.stage_id.id == 14 and self.product_type == "3":
                if self.rejection_note:
                    self['state']='reject'
                    self['description'] =   str(self.description) + " " +' ● '+  str(self.rejection_note) + ' ' + '('+ str(self.related_stage_name) + ')' + '\n '
                    self['rejection_note'] = False
                    self['stage_id'] = 12
                    self['state'] ='pending'
            elif self.stage_id.id == 14:
                if self.rejection_note:
                    self['state']='reject'
                    self['description'] =   str(self.description) + " " +' ● '+  str(self.rejection_note) + ' ' + '('+ str(self.related_stage_name) + ')' + '\n '
                    self['rejection_note'] = False
                    self['stage_id'] = 10
                    self['state'] ='pending'
                else:
                    raise UserError('Please Enter The Rejection Note')
        elif self.team_id.id == 1:
            if self.stage_id.id == 5:
                if self.rejection_note:
                    self['state']='reject'
                    self['description'] =  ' ● '+  str(self.rejection_note) + ' ' +'('+ str(self.related_stage_name) + ')' + '\n' 
                    self['rejection_note'] = False
                else:
                    raise UserError('Please Enter The Rejection Note')
            elif self.stage_id.id == 7:
                self['company_structure'] = False
                self['business_type'] = False
                self['monthly_revenue'] = False
                self['_no_of_years_'] = False
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
                    self['stage_id'] = 5
                    self['state'] ='pending'
                else:
                    raise UserError('Please Enter The Rejection Note')
            elif self.stage_id.id == 9:
                if self.rejection_note:
                    self['state']='reject'
                    self['description'] =  str(self.description) + " " +' ● '+  str(self.rejection_note) + ' ' + '('+ str(self.related_stage_name) + ')' + '\n '
                    self['rejection_note'] = False
                    self['stage_id'] = 7
                    self['state'] ='pending'
                else:
                    raise UserError('Please Enter The Rejection Note')
            elif self.stage_id.id == 11:
                if self.rejection_note:
                    self['state']='reject'
                    self['description'] =   str(self.description) + " " +' ● '+  str(self.rejection_note) + ' ' + '('+ str(self.related_stage_name) + ')' + '\n '
                    self['rejection_note'] = False
                    self['stage_id'] = 9
                    self['state'] ='pending'
                else:
                    raise UserError('Please Enter The Rejection Note')
            elif self.stage_id.id == 13 and self.product_type == "3":
                if self.rejection_note:
                    self['state']='reject'
                    self['description'] =   str(self.description) + " " +' ● '+  str(self.rejection_note) + ' ' + '('+ str(self.related_stage_name) + ')' + '\n '
                    self['rejection_note'] = False
                    self['stage_id'] = 11
                    self['state'] ='pending'
            elif self.stage_id.id == 12:
                if self.rejection_note:
                    self['state']='reject'
                    self['description'] =   str(self.description) + " " +' ● '+  str(self.rejection_note) + ' ' + '('+ str(self.related_stage_name) + ')' + '\n '
                    self['rejection_note'] = False
                    self['stage_id'] = 9
                    self['state'] ='pending'
                else:
                    raise UserError('Please Enter The Rejection Note')

            # if self.product_type == '1' and self.state == "reject" :
            #     self['partner_id']['approve_for_BL'] = False
            # elif self.product_type == '2' and self.state == "reject":
            #     self['partner_id']['approve_for_DTL'] = False
            # elif self.product_type == '3' and self.state == "reject":
            #     self['partner_id']['approve_for_ID'] = False
        
        # raise UserError("Helllo")
    # "Drive-Through Lending" "Working Capital Lending"
    # bilal Commit here for checking 
    # @api.onchange('product_type','partner_id')
    # def partner_id_domain_pur(self):
    #     if self.product_type == '1': 
    #         return {"domain": {'partner_id': [('state', '=', 'approve')]}}
    #     return {"domain": {'partner_id': []}}

    def action_create_invoice(self):
        lines = []
        interestlines = []
        product_id = 0
        if self.product_type == '1':
            product_id = 1
        elif self.product_type == '2':
            product_id = 2
        elif self.product_type == '3':
            product_id = 3
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
                    commission_by_day = (self.applicable_interest_rate / float(30)) * float(final_date)
                    commission_value = (self.approved_loan_amount / 100) * commission_by_day
                    lines.append((0,0,{
                        'product_id':product_id,
                        # 'account_id' : income_account.id,
                        'quantity':1,
                        'price_unit' : rec.approved_loan_amount
                    }))
                    lines.append((0,0,{
                        'product_id': 4,
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
    instrument_number = fields.Char(string="Post dated Instrument Number")
    instrument_due_date = fields.Date(string="Post Dated Instrument Due Date")
    instrument_amount = fields.Float(string="Attach Post Dated Amount")
    instrument_document = fields.Binary(string="Attach Post Dated Instrument")
    instrument_document_name = fields.Char(string="Attach Post Dated Instrument")

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
    default_under_writing_authority  = fields.Selection([('Meezan Bank Limited', 'Meezan Bank Limited'), ('Bank Al Habib', 'Bank Al Habib'),('Trukkr Financial Services', 'Trukkr Financial Services')], string= "Default Under Writing Authority" )

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
                        if invline.product_id.id == 1 or invline.product_id.id == 2 or invline.product_id.id == 3:
                            
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
    cnic = fields.Char(string="Cnic#",required=True)
    designation =fields.Char(string="Designation",required=True)
    contact_no = fields.Char(string = "Contact No",required=True)
    email_address = fields.Char(string = "Email Address")
    address = fields.Char(string = "Address")
class AuthorizedSignatoryDetails(models.Model):
    _name = 'authorized.signatory.details'
    _description = 'Authorized Signatory Details'

    crm_id = fields.Many2one('crm.lead')
    full_name = fields.Char(string="Full Name",required=True)
    cnic = fields.Char(string="Cnic#",required=True)
    designation =fields.Char(string="Designation",required=True)
    contact_no = fields.Char(string = "Contact No",required=True)
    email_address = fields.Char(string = "Email Address")
    address = fields.Char(string = "Address")
class DetailsOfDirectorShareHolder(models.Model):
    _name = 'details.of.director.share.holder'
    _description = 'Details of Director / Share Holder'

    crm_id = fields.Many2one('crm.lead')
    full_name = fields.Char(string="Full Name",required=True)
    cnic = fields.Char(string="Cnic#",required=True)
    share_of_hold = fields.Float(string="'%' of Shares Held")
    designation =fields.Char(string="Designation",required=True)
    contact_no = fields.Char(string = "Contact No",required=True)
    email_address = fields.Char(string = "Email Address")
    address = fields.Char(string = "Address")

class MultiDocCRM(models.Model):
    _name = "multi.documents.crm"

    # partner_id = fields.Many2one('res.partner')
    crm_id = fields.Many2one('crm.lead')

    uploader_name = fields.Char(string="Document Name")
    url = fields.Binary(string="Document")
    url_name = fields.Char(string="Document")
    description = fields.Char(string="Description")
    date = fields.Date(string="Date")