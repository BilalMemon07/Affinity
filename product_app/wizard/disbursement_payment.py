from odoo import fields, models
from odoo.exceptions import UserError


class DisbursementPayment(models.TransientModel):
    _name = 'disbursement.payment'
    _description = 'Disbursement Payment'
    journal = fields.Many2one('account.journal',requird = True,string='Journal',domain = [('type','in',('bank','cash'))] )
    payment_date = fields.Date(string = "Payment Date")

    def create_disbursement(self):
        # raise UserError("hea")
        if self.journal:
            invoice = self.env['account.move'].browse(
                self._context.get('active_ids', [])
            )
            invoice.disbursement_payment()
            disbursement = self.env['account.disbursement'].search([('invoice_id','=', invoice.id)])
            # raise UserError(disbursement)
            for dis in disbursement:
                dis.write({
                    'journal_id': self.journal.id
                })
        # # if self.rejection_note:
        # crm_lead['rejection_note'] = self.rejection_note
        # crm_lead.reject_action()
        # else:
            # raise UserError('Please Enter The Rejection Note')

            