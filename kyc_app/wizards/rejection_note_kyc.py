from odoo import fields, models
from odoo.exceptions import UserError


class RejectionNote(models.TransientModel):
    _name = 'rejection.note.kyc'
    _description = 'Rejection Note'
    rejection_note = fields.Char(string='Rejection Note')

    def reject(self):
        res_partner = self.env['res.partner'].browse(
            self._context.get('active_ids', [])
        )
        if res_partner['rejection_note'] == False:
            res_partner.reject_action()
            res_partner['rejection_note'] = self.rejection_note.strip()
        else:
            res_partner['rejection_note'] += self.rejection_note + "\n"
            # res_partner['rejection_note'] += self.rejection_note
            res_partner.reject_action()
