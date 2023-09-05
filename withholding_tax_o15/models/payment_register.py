# Bilal
from odoo import api, fields, models, _,Command
from odoo.exceptions import UserError
from odoo.addons.account.wizard.account_payment_register import AccountPaymentRegister as ARP

class PaymentRegister(models.TransientModel):
    _inherit = 'account.payment.register'
    _description = 'Register Payment'

    amount_to_withhold = fields.Float(string="Amount to Withhold")
    tax_code = fields.Many2one('account.tax', string='Tax Code', domain=[('is_withholding', '=', True)])
    tax_account = fields.Many2one('account.account', string='Tax Account')
    tax_perc = fields.Float(string='Tax %', readonly=True)
    tax_amount = fields.Float(string='Tax Amount', readonly=True)
    total_amount = fields.Float(string='Total Amount', readonly=True)


    amount_to_withhold_service = fields.Float(string="Amount to Withhold")
    paid_to_service = fields.Monetary(string='Paid to', store=True, readonly=True)
    tax_code_service = fields.Many2one('account.tax', string='Tax Code', domain=[('is_withholding', '=', True)])
    tax_account_service = fields.Many2one('account.account', string='Tax Account', readonly=True)
    tax_perc_service = fields.Float(string='Tax %', readonly=True)
    tax_amount_service = fields.Float(string='Tax Amount', readonly=True)
    total_amount_service = fields.Float(string='Total Amount', readonly=True)


    @api.onchange('tax_code' , 'tax_code_service')
    def _compute_tax_fields(self):
        for record in self:
            for data in record.tax_code.invoice_repartition_line_ids:
                if self.amount_to_withhold:
                    record.tax_account = data.account_id.id
                    record.tax_perc = 	record.tax_code.amount
                    record.tax_amount = round(record.amount_to_withhold * (record.tax_perc / 100))
                    record.total_amount = round(record.amount_to_withhold - record.tax_amount)

            for dat in record.tax_code_service.invoice_repartition_line_ids:
                if self.amount_to_withhold_service:
                    record.tax_account_service = dat.account_id.id
                    record.tax_perc_service = 	record.tax_code_service.amount
                    record.tax_amount_service = round(record.amount_to_withhold_service * (record.tax_perc_service / 100))
                    record.total_amount_service = round(record.amount_to_withhold_service - record.tax_amount_service)
                # record.paid_to = record.amount + record.tax_amount
                # record.paid_to = record.amount + record.tax_amount

    @api.onchange('amount')
    def _onchange_amounts(self):
        for record in self:
            record.tax_code = False
            record.tax_account = False
            record.tax_perc = 	False
            record.tax_amount = False
            record.total_amount = False

            record.tax_code_service = False
            record.tax_account_service = False
            record.tax_perc_service = 	False
            record.tax_amount_service = False
            record.total_amount_service = False
            # record.paid_to = False

    
    def _create_payment_vals_from_wizard(self):
        payment_vals = {
            'date': self.payment_date,
            'amount': self.amount,
            'payment_type': self.payment_type,
            'partner_type': self.partner_type,
            'ref': self.communication,
            'journal_id': self.journal_id.id,
            'currency_id': self.currency_id.id,
            'partner_id': self.partner_id.id,
            'partner_bank_id': self.partner_bank_id.id,
            'payment_method_line_id': self.payment_method_line_id.id,
            'destination_account_id': self.line_ids[0].account_id.id,
            'x_studio_payment_mode': self.x_studio_payment_mode,
            'x_studio_cheque_no': self.x_studio_cheque_no,

             # WHT
            'amount_to_withhold':self.amount_to_withhold,
            'tax_code':self.tax_code.id,
            'tax_account':self.tax_account.id,
            'tax_perc':self.tax_perc,
            'tax_amount':self.tax_amount,
            'total_amount' : self.total_amount,

            # wht services
            'amount_to_withhold_service' : self.amount_to_withhold_service,
            'tax_code_service':self.tax_code_service.id,
            'tax_account_service':self.tax_account_service.id,
            'tax_perc_service':self.tax_perc_service,
            'tax_amount_service':self.tax_amount_service,
            'total_amount_service':self.total_amount_service,


            
            'paid_to' : self.amount + self.tax_amount + self.tax_amount_service
        }

        if not self.currency_id.is_zero(self.payment_difference) and self.payment_difference_handling == 'reconcile':
            payment_vals['write_off_line_vals'] = {
                'name': self.writeoff_label,
                'amount': self.payment_difference,
                'account_id': self.writeoff_account_id.id,
            }
        return payment_vals




       
# AccountRigisterPayment

    ARP._create_payment_vals_from_wizard = _create_payment_vals_from_wizard
