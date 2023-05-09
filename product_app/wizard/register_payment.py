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



            