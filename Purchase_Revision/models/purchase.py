from odoo import api, fields, models, _
from odoo.exceptions import AccessError, UserError, ValidationError

class PurchaseOrder(models.Model):
    _inherit = "purchase.order"
   
    current_revision_id = fields.Many2one('purchase.order','Current revision',readonly=True,copy=True)
    old_revision_ids = fields.One2many('purchase.order','current_revision_id','Old revisions',readonly=True,context={'active_test': False})
    revision_number = fields.Integer('Revision',copy=False)
    unrevisioned_name = fields.Char('Order Reference',copy=False,readonly=True)
    active = fields.Boolean('Active',default=True,copy=True) 
    revised = fields.Boolean('Revised Quotation')
    
    @api.model
    def create(self, vals):
        if 'unrevisioned_name' not in vals:
            if vals.get('name', 'New') == 'New':
                seq = self.env['ir.sequence']
                vals['name'] = seq.next_by_code('purchase.order') or '/'
            vals['unrevisioned_name'] = vals['name']
#             vals['revised'] = True
        return super(PurchaseOrder, self).create(vals)
    
    
    def action_revision(self):
        self.ensure_one()
        view_ref = self.env['ir.model.data'].check_object_reference('purchase', 'purchase_order_form')
        view_id = view_ref and view_ref[1] or False,
        self.with_context(sale_revision_history=True).copy()
        self.write({'state': 'draft'})
        self.order_line.write({'state': 'draft'})
#            self.mapped('order_line').write(
#                {'sale_line_id': False})
        return {
            'type': 'ir.actions.act_window',
            'name': _('Purchase Order'),
            'res_model': 'purchase.order',
            'res_id': self.id,
            'view_type': 'form',
            'view_mode': 'form',
            'view_id': view_id,
            'target': 'current',
            'nodestroy': True,
        }
        
    @api.returns('self', lambda value: value.id)
    def copy(self, defaults=None):
        if not defaults:
            defaults = {}
        if not self.unrevisioned_name:
            self.unrevisioned_name = self.name
        if self.env.context.get('sale_revision_history'):
            prev_name = self.name
            revno = self.revision_number
            self.write({'revision_number': revno + 1,'name': '%s-%02d' % (self.unrevisioned_name,revno + 1)})
            defaults.update({'name': prev_name,'revision_number': revno,'revised':True,'active': True,'state': 'cancel','current_revision_id': self.id,'unrevisioned_name': self.unrevisioned_name,})
        return super(PurchaseOrder, self).copy(defaults)