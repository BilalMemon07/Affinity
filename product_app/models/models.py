# -*- coding: utf-8 -*-
from odoo import models, fields, api, _
from odoo.exceptions import UserError
from datetime import datetime
    


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

    interest_rate = fields.Float(string= "Interest Rate") 

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
    crm_count = fields.Integer(string='Invoice', compute='get_crm_count')
    
    def get_crm_count(self):
        count = self.env['account.move'].search_count([('crm_id', '=', self.id)])
        self.crm_count = count  

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
        if self.product_type == '1' or self.product_type == '3':
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
                self['stage_id'] = 7
                # self['state'] ='pending'
        else:
            self['state'] = 'approve'
            self['stage_id'] = 8
        
        
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

    def action_create_invoice(self):
        lines = []
        commisiionlines = []
        for rec in self:
            commission_value = 20000
            income_account = self.env['account.account'].search([('code', '=', "3111001")])
            # receivable_account = self.env['account.account'].search([('code', '=', "1121001")])
            commission_account = self.env['account.account'].search([('code', '=', "4311002")])
            # raise UserError(str(income_account.name) + ', ' + str(receivable_account.name) + ', ' + str(commission_account.name))
            lines.append((0,0,{
                'product_id': 1,
                'account_id' : income_account.id,
                'quantity':1,
                'price_unit' : 120000
            }))
            commisiionlines.append((0, 0,
                {
                'account_id': commission_account.id,
                'credit': commission_value,
                'exclude_from_invoice_tab': True
                }
            ))
            move = self.env['account.move'].create({
            'journal_id': 1,
            'invoice_date': datetime.now(),
            'invoice_date_due': datetime.now(),
            'invoice_line_ids':lines,
            'move_type':'out_invoice',
            'partner_id' : rec.partner_id.id,
            'crm_id': rec.id,
            })
            move.with_context(check_move_validity=False).write({
                'line_ids' : commisiionlines
            })
            for line in move.line_ids:
                if line.account_id == income_account:
                    line['credit'] = line.credit-commission_value
                    break
 
    
    
      # move.action_post()       


class AccountMove(models.Model):
    _inherit = 'account.move'

    crm_id = fields.Many2one('crm.lead' , string="CRM")

    def disbursement_payment(self):
        for rec in self:
            if rec.state == 'posted':
                payment_obj = rec.env['account.payment']
                # sale_order = rec.env['sale.order'].search([('name','=',rec.invoice_origin)])
                # delivery_order = rec.env['stock.picking'].search([('origin','=',sale_order.name)])
                # for dev_line in delivery_order:
                # if sale_order:
                    # if dev_line['x_studio_courier'] == "Courier":
                        # if dev_line['x_studio_payment_type'] == "Cash" or dev_line['x_studio_payment_type'] == False:
                journal = self.env['account.journal'].search([('id', '=', 7)])
                payment_obj.create({
                    'partner_id': rec.partner_id.id,
                    'payment_type' : 'outbound',
                    'partner_type' : 'customer',
                    'destination_account_id' : 32,
                    # 'journal_id' : rec.journal_id.id,
                    # 'payment_method_id':4,
                    'date':datetime.now() ,
                    # 'payment_method_line_id': 2,#journal.outbound_payment_method_line_ids[0].id,
                    'amount': rec.amount_total,
                    })

