# -*- coding: utf-8 -*-
from odoo import api, fields, models,_
from odoo.exceptions import UserError
from datetime import datetime

class RecordExpense(models.Model):
    _name = "expense.module"
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _description = "Expense Module"

    name = fields.Char(string='Record Expense Reference', required=True, copy=False, readonly=True,
                           index=True, default=lambda self: _('New'))
    paid_to = fields.Char(string='Paid To' ,copy=True)
    journal = fields.Many2one('account.journal',string='Journal' ,copy=True)
    account_id = fields.Many2one('account.account',string='Account', copy=True)
    currency_id = fields.Many2one('res.currency',string='Currency',copy=True,  related='journal.company_id.currency_id',
                                 default=lambda
                                 self: self.env.user.company_id.currency_id.id)
    memo = fields.Text(string='Memo', copy=True)
    is_posted = fields.Char(string='Is Posted' ,copy=True)
    posting_date = fields.Date(string='Posting Date')
    date = fields.Date(string='Accounting Date')
    cheque_date = fields.Date(string='Cheque Date')
    cheque_number = fields.Char(string='Cheque Number',copy=True)
    total_expense = fields.Monetary(string='Total Expense',copy=True)
    # expense_amount_in_words = fields.Char(string='Expense Amount In Words', readonly=True)
    expense_line = fields.One2many('expense.line', 'expense_module_id',copy=True ,string="Expense Line")
    state = fields.Selection([('draft', 'Draft'), ('posted', 'Posted')], string='Status')
    expense_count = fields.Integer(string='Journal Entry', compute='get_expense_count')

    # def amount_in_words(self):
    #     self.expense_amount_in_words = str(self.currency_id.amount_to_text(self.total_expense)) + ' only'
    
    
    
    @api.onchange("journal")
    def get_account_by_journal(self):
        if self.journal.id:
            if self.journal.is_miscellaneous_journal:
                self['account_id'] = self.journal.default_account_id.id
                # raise UserError("sa")
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
    @api.onchange("expense_line")
    def compute_line_item(self):
        sub_total = 0
        for line in self.expense_line:
            sub_total += line.value
            
        self.total_expense = sub_total
        
    
    def get_expense_count(self):
        count = self.env['account.move'].search_count([('expense_id', '=', self.id)])
        self.expense_count = count
    
    @api.model
    def create(self,vals):
        if vals.get('name', _('New')) == _('New'):
            vals['name'] = self.env['ir.sequence'].next_by_code('Exp_Seq') or _('New')
            vals['state']='draft'
            vals['posting_date'] = datetime.now()
            vals['date'] = datetime.now()
        res = super(RecordExpense,self).create(vals)
        return res
    
    # # @api.model
    # @api.model
    # def write(self,vals,a):
    #     # vals['total_expense']=self.total_expense
    #     exp=self.env['expense.module'].update({
    #             'total_expense': self.total_expense,
    #             })
    #     # res = super(RecordExpense,self).update(vals)
    #     # return res

    def server_post_expense_action(self):
        lines = []
        for rec1 in self:
            if rec1.state == 'posted':
                raise UserError('This Document is already posted')
            else:
                credit = 0
                for rec in rec1.expense_line:
                    credit += rec.value
                    line = (0, 0, {
                        'account_id': rec.account.id,
                        'debit': rec.value,
                        'name':rec.description,
                        'partner_id': rec.partner.id,
                        'analytic_distribution': rec.analytical_field,
                        # 'analytic_tag_ids': rec.tags,
                    })
                    lines.append(line)
                line_ = (0, 0, {
                    'account_id': rec1.journal.default_account_id.id if rec1.journal.is_miscellaneous_journal else rec1.account_id.id ,
                    'credit': credit,
                    'name':rec1.name,
                    'partner_id': rec.partner.id,
                    })
                lines.append(line_)
                # raise UserError(str(lines))
                
                move = self.env['account.move'].with_context(check_move_validity=False).create({
                'journal_id': rec1.journal.id,
                'date': rec1.date,
                'line_ids': lines,
                'ref': rec1.name,
                'expense_id': rec1.id, 
                })

                # if move:
                #     move.write({
                #     })
                # raise UserError(str(lines))
                # for move_line in move.line_ids:
                #     for rec_line in rec1.expense_line:
                #         if move_line.account_id == rec_line.account:
                #             move_line.write({
                #                 'name' : rec_line['description']
                #             })
                            # raise UserError(rec_line['description'])
                rec1.write({
                'state': 'posted',
                'is_posted': '1',
                })
                # move.action_post()
                
class AccountMove(models.Model):
    _inherit = 'account.move'
    expense_id = fields.Many2one('expense.module',string='Expense')
    cheque_number = fields.Char(string='Cheque Number')
    
    @api.model
    def getChequeNo(self):
        for rec in self:
            if rec.expense_id:
                rec['cheque_number'] = rec.expense_id.cheque_number
            elif rec.payment_id:
                rec['cheque_number'] = rec.payment_id.check_number
            

    # def button_draft(self):
    #     expense = self.env['expense.module'].search([('id','=',self.expense_id.id)])
    #     if expense:
    #         expense.write({
    #             'state': 'draft',
    #             'is_posted': '0',
    #             })
    #     res = super(AccountMove, self).button_draft()
    #     return res
class AccountJournal(models.Model):
    _inherit = 'account.journal'
    is_miscellaneous_journal = fields.Boolean(string = 'Is Miscellaneous Journal')


class ExpenseLine(models.Model):
    _name = 'expense.line'
    _description = "Expense Line"

    expense_module_id = fields.Many2one('expense.module')
    account = fields.Many2one('account.account',string='Account')
    description = fields.Char(string='Short Description')
    partner = fields.Many2one('res.partner',string='Partner')
    # tags = fields.Many2one('account.analytic.account',string='Tags')
    analytic_precision = fields.Integer(string='Analytic Precision')

    analytic_line_ids = fields.One2many(
        comodel_name='account.analytic.line', inverse_name='move_line_id',
        string='Analytic lines',
    )
    analytical_field=fields.Json()

    currency_id = fields.Many2one('res.currency',string='Currency', related='account.company_id.currency_id',
                                 default=lambda
                                 self: self.env.user.company_id.currency_id.id)
    value = fields.Monetary(string='Value')
    
    # @api.onchange('analytic_distribution')
    # def _inverse_analytic_distribution(self):
    #     """ Unlink and recreate analytic_lines when modifying the distribution."""
    #     lines_to_modify = self.env['account.move.line'].browse([
    #         line.id for line in self if line.parent_state == "posted"
    #     ])
    #     lines_to_modify.analytic_line_ids.unlink()
    #     lines_to_modify._create_analytic_lines()

    def _compute_currency_id(self):
        for pay in self:
            pay.currency_id = pay.journal_id.currency_id or pay.journal_id.company_id.currency_id
