# -*- coding: utf-8 -*-
from odoo import api, fields, models,_
from odoo.exceptions import UserError

class RecordExpense(models.Model):
    _name = "expense_module"
    _description = "Expense Module"

    name = fields.Char(string='Record Expense Reference', required=True, copy=False, readonly=True,
                           index=True, default=lambda self: _('New'))
    paid_to = fields.Char(string='Paid To')
    journal = fields.Many2one('account.journal',string='Journal')
    currency_id = fields.Many2one('res.currency',string='Currency',  related='journal.company_id.currency_id',
                                 default=lambda
                                 self: self.env.user.company_id.currency_id.id)
    memo = fields.Text(string='Memo')
    is_posted = fields.Char(string='Is Posted')
    posting_date = fields.Date(string='Posting Date')
    date = fields.Date(string='Accounting Date', required=True)
    cheque_date = fields.Date(string='Cheque Date',)
    cheque_number = fields.Char(string='Cheque Number')
    total_expense = fields.Monetary(string='Total Expense',)
    expense_amount_in_words = fields.Char(string='Expense Amount In Words', readonly=True,compute='amount_in_words')
    expense_line = fields.One2many('expense_line', 'expense_module_id', string="Expense Line")
    state = fields.Selection([('draft', 'Draft'), ('posted', 'Posted')], string='Status')
    expense_count = fields.Integer(string='Journal Entry', compute='get_expense_count')

    def amount_in_words(self):
        self.expense_amount_in_words = str(self.currency_id.amount_to_text(self.total_expense)) + ' only'

   
    def open_patient_appointment(self):
        return {
            'name': 'Journal Entry',
            'domain': [('expense_id', '=', self.id)],
            'view_type': 'form',
            'res_model': 'account.move',
            'view_id': False,
            'view_mode': 'tree,form',
            'type': 'ir.actions.act_window'
        }
    
    def get_expense_count(self):
        count = self.env['account.move'].search_count([('expense_id', '=', self.id)])
        self.expense_count = count
    
    @api.model
    def create(self,vals):
        if vals.get('name', _('New')) == _('New'):
            vals['name'] = self.env['ir.sequence'].next_by_code('Exp_Seq') or _('New')
            vals['state']='draft'
        res = super(RecordExpense,self).create(vals)
        return res
    
    def server_post_expense_action(self):
        for rec1 in self:
            if rec1.state == 'posted':
                raise UserError('This Document is already posted')
            else:
                lines = []
                credit = 0
                for rec in rec1.expense_line:
                    credit += rec.value
                    line = (0, 0, {
                        'account_id': rec.account.id,
                        'debit': rec.value,
                        'partner_id': rec.partner.id,
                        'analytic_tag_ids': rec.tags,
                    })
                    lines.append(line)
                line = (0, 0, {
                    'account_id': rec1.journal.default_account_id.id,
                    'credit': credit,
                    })
                lines.append(line)
                
                move = self.env['account.move'].create({
                'journal_id': rec1.journal.id,
                'date': rec1.date,
                'line_ids': lines,
                'ref': rec1.name,
                'expense_id': rec1.id,
                })
                rec1.write({
                'state': 'posted',
                'is_posted': '1',
                })
                move.action_post()
                
class AccountMove(models.Model):
    _inherit = 'account.move'
    expense_id = fields.Many2one('expense_module',string='Expense')
    
    def button_draft(self):
        expense = self.env['expense_module'].search([('id','=',self.expense_id.id)])
        if expense:
            expense.write({
                'state': 'draft',
                'is_posted': '0',
                })
        res = super(AccountMove, self).button_draft()
        return res
         
class ExpenseLine(models.Model):
    _name = 'expense_line'
    _description = "Expense Line"

    expense_module_id = fields.Many2one('expense_module')
    account = fields.Many2one('account.account',string='Account')
    description = fields.Char(string='Short Description')
    partner = fields.Many2one('res.partner',string='Partner')
    tags = fields.Many2one('account.analytic.tag',string='Tags')
    currency_id = fields.Many2one('res.currency',string='Currency', related='account.company_id.currency_id',
                                 default=lambda
                                 self: self.env.user.company_id.currency_id.id)
    value = fields.Monetary(string='Value')

    def _compute_currency_id(self):
        for pay in self:
            pay.currency_id = pay.journal_id.currency_id or pay.journal_id.company_id.currency_id