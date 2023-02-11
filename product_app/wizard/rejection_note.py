from odoo import fields, models
from odoo.exceptions import UserError


class RejectionNote(models.TransientModel):
    _name = 'rejection.note'
    _description = 'Rejection Note'
    rejection_note = fields.Char(string='Rejection Note')

    def reject(self):
        crm_lead = self.env['crm.lead'].browse(
            self._context.get('active_ids', [])
        )
        # if self.rejection_note:
        crm_lead['rejection_note'] = self.rejection_note
        crm_lead.reject_action()
        # else:
            # raise UserError('Please Enter The Rejection Note')

            