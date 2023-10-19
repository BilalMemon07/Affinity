# -*- coding: utf-8 -*-

from odoo import models, fields, api
from odoo.exceptions import UserError
import datetime

class AccountMove(models.Model):
    _inherit = 'account.move'
    
    total_commission = fields.Float(string="Total Commission" , compute = "compute_total_commsission")
    invoice_id = fields.Many2one('account.move', string="Invoice ID")

    jv_count = fields.Integer(string='Journal Entry', compute='get_jv_count')

    def get_jv_count(self):
        count = self.env['account.move'].search_count([('invoice_id', '=', self.id)])
        self.jv_count = count  
    

    def open_journal_enrty(self):
        return {
            'name': 'Journal Entry',
            'domain': [('invoice_id', '=', self.id)],
            'view_type': 'form',
            'res_model': 'account.move',
            'view_id': False,
            'view_mode': 'tree,form',
            'type': 'ir.actions.act_window'
        }

    @api.depends('invoice_line_ids','invoice_line_ids.total_commission')
    def compute_total_commsission(self):
        for rec in self:
            rec['total_commission'] = 0 
            if rec.invoice_line_ids:
                total_sum = sum(item['total_commission'] for item in rec.invoice_line_ids)
                rec['total_commission'] = total_sum

    
    def action_post(self):
        res = super(AccountMove, self).action_post()
        for rec in self:
            if rec.total_commission:
                # raise UserError(str(rec.company_id.commission_account_id.id) + "and" + str(rec.company_id.discount_account_id.id) + "and" + str(rec.company_id.journal_id.id))
                if rec.company_id.commission_account_id.id and rec.company_id.discount_account_id.id and rec.company_id.journal_id.id:
                    journal_entry_line = []
                    journal_entry_line.append((0,0,{
                        'account_id': rec.company_id.discount_account_id.id,
                        'debit' : rec.total_commission,
                        'name' : rec.name,
                    }))
                    journal_entry_line.append((0,0,{
                        'account_id': rec.company_id.commission_account_id.id,
                        'credit' : rec.total_commission,
                        'name' : rec.name,
                    }))
                    obj = {
                        'date': datetime.datetime.now(),
                        'line_ids': journal_entry_line,
                        'journal_id' : rec.company_id.journal_id.id,
                        'ref':rec.name,
                        'invoice_id' : rec.id,
                        'move_type':'entry'

                    }
                    self.env['account.move'].create(obj)
                else:
                    raise UserError("check again")

        return res


class AccountMoveLine(models.Model):
    _inherit = 'account.move.line'
    

    commission = fields.Float(string="Commission" , compute="compute_commission")
    total_commission = fields.Float(string="Total Commission" , compute="compute_total_commission")
    
    @api.depends('product_id')
    def compute_commission(self):
        for rec in self:
            rec['commission'] = 0
            if rec.product_id:
                if rec.product_id.product_tmpl_id.commission:
                    rec['commission'] = rec.product_id.product_tmpl_id.commission 
    
    @api.depends('commission','quantity')
    def compute_total_commission(self):
        for rec in self:
            rec['total_commission'] = 0
            if rec.product_id:
                if rec.commission:
                    rec['total_commission'] = rec.commission * rec.quantity


    
    

    



    
 

                