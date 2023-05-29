from odoo import fields, models
from odoo.exceptions import UserError


class RegisterPayment(models.TransientModel):
    _name = 'register.payment'
    _description = 'Register Payment'
    
    journal_id = fields.Many2one('account.journal',requird = True,string='Journal',domain = [('type','in',('bank','cash'))] )
    payment_method = fields.Many2one('account.payment.method.line',string="Payment Method")
    currency_id = fields.Many2one(
        'res.currency', string='Currency')
    amount = fields.Monetary(string="Amount",currency_field="currency_id")
    payment_date = fields.Date(string="Payment Date")
    memo = fields.Char(string="Memo")
    transaction_id = fields.Char(string="Transaction id")


    def get_payment_vals_custom(self):
        invoice = self.env['account.move'].browse(
                self._context.get('active_ids', [])
        )
        intrest_amount = 0
        for line in invoice.invoice_line_ids:
            if line.product_id.id == 4:
                intrest_amount += line.price_unit
        # loan_amount = invoice.amount_total_in_currency_signed - intrest_amount
        
        payment_method_line = self.journal_id._get_available_payment_method_lines("inbound")[:1]
        if self.amount > invoice.x_studio_remaining_intrest and invoice.x_studio_remaining_intrest > 0:
            payment_amount =  self.amount -  invoice.x_studio_remaining_intrest
            # raise UserError(payment_amount)
            payment_id_1 = self.env['account.payment'].create({
                'date': self.payment_date,
                'amount': payment_amount,
                'payment_type': 'inbound',
                'partner_type': "customer",
                'ref': invoice.name,
                'journal_id': self.journal_id.id,
                'currency_id': invoice.currency_id.id,
                'partner_id': invoice.partner_id.id,
                'partner_bank_id': self.journal_id.bank_account_id.id,
                'payment_method_line_id': payment_method_line.id,
                'destination_account_id': 17,
                'transaction_id':self.transaction_id
            })
            payment_id_1.action_post()
            receivable_line_1 = payment_id_1.line_ids.filtered('credit')
            invoice.js_assign_outstanding_line(receivable_line_1.id)
            payment_id_2 = self.env['account.payment'].create({
                'date': self.payment_date,
                'amount': invoice.x_studio_remaining_intrest,
                'payment_type': 'inbound',
                'partner_type': "customer",
                'ref': invoice.name,
                'journal_id': self.journal_id.id,
                'currency_id': invoice.currency_id.id,
                'partner_id': invoice.partner_id.id,
                'partner_bank_id': self.journal_id.bank_account_id.id,
                'payment_method_line_id': payment_method_line.id,
                'destination_account_id': 95,
                'transaction_id':self.transaction_id
            })
            payment_id_2.action_post()
            receivable_line_2 = payment_id_2.line_ids.filtered('credit')
            invoice.js_assign_outstanding_line(receivable_line_2.id)
            invoice['x_studio_remaining_intrest'] =  payment_amount - invoice['x_studio_remaining_intrest']
        elif self.amount <= intrest_amount and invoice.x_studio_remaining_intrest > 0:
            payment_id_3 = self.env['account.payment'].create({
                'date': self.payment_date,
                'amount': self.amount,
                'payment_type': 'inbound',
                'partner_type': "customer",
                'ref': invoice.name,
                'journal_id': self.journal_id.id,
                'currency_id': invoice.currency_id.id,
                'partner_id': invoice.partner_id.id,
                'partner_bank_id': self.journal_id.bank_account_id.id,
                'payment_method_line_id': payment_method_line.id,
                'destination_account_id': 95,
                'transaction_id':self.transaction_id
            })
            invoice['x_studio_remaining_intrest'] = invoice['x_studio_remaining_intrest'] - self.amount
            payment_id_3.action_post()
            receivable_line_3 = payment_id_3.line_ids.filtered('credit')
            invoice.js_assign_outstanding_line(receivable_line_3.id)
        elif self.amount <= invoice.amount_residual and invoice.x_studio_remaining_intrest <= 0:
            payment_id_4 = self.env['account.payment'].create({
                'date': self.payment_date,
                'amount': self.amount,
                'payment_type': 'inbound',
                'partner_type': "customer",
                'ref': invoice.name,
                'journal_id': self.journal_id.id,
                'currency_id': invoice.currency_id.id,
                'partner_id': invoice.partner_id.id,
                'partner_bank_id': self.journal_id.bank_account_id.id,
                'payment_method_line_id': payment_method_line.id,
                'destination_account_id': 17,
                'transaction_id':self.transaction_id
            })
            payment_id_4.action_post()
            receivable_line_4 = payment_id_4.line_ids.filtered('credit')
            invoice.js_assign_outstanding_line(receivable_line_4.id)
        elif self.amount >  invoice.amount_residual:
            raise UserError('Amount is not greater then invoice due amount')
        
        # raise UserError(str(vals))
    # def action_create_payment_custom(self):



            