# -*- coding: utf-8 -*-

from odoo import models, fields, api
from odoo.exceptions import UserError
from odoo.tools import config, human_size, ImageProcess, str2bool, consteq
import base64

# from odoo.addons.base.models.ir_attachment import IrAttachment as IA



DELIVERY_STATUS = [
    ('pending', 'Not Delivered'),
    ('partial', 'Partially Delivered'),
    ('full', 'Fully Delivered'),
]

# class IrAttachments(models.Model):
#     _inherit = 'ir.attachment'

#     image_base_64 = fields.Char(string="Image Base 64")

#     def _compute_datas(self):
#         if self._context.get('bin_size'):
#             for attach in self:
#                 attach.datas = human_size(attach.file_size)
#             return

#         # bilal
#         for attach in self:
#             # raise UserError(attach.raw)
#             attach.datas = base64.b64encode(attach.raw or b'')
#             self['image_base_64'] = attach.datas

#     IA._compute_datas = _compute_datas
    


class SaleOrderLine(models.Model):
    _inherit = 'sale.order.line'
    

    delivery_status = fields.Selection(selection=DELIVERY_STATUS,string="Delivery Status",store=True)
    # documents = fields.Binary('Documents')
    # attachment_ids = fields.Many2many('l', string='Attachments')


    @api.depends('qty_delivered_method',
        'analytic_line_ids.so_line',
        'analytic_line_ids.unit_amount',
        'analytic_line_ids.product_uom_id')
    def _compute_qty_delivered(self):
        result = super(SaleOrderLine,self)._compute_qty_delivered()
        for rec in self:
            if rec.qty_delivered == rec.product_uom_qty:
                rec['delivery_status'] = "full"
            elif rec.qty_delivered <= 0:
                rec['delivery_status'] = "pending"
            elif rec.qty_delivered >= 0:
                rec['delivery_status'] = "partial"
        
        
        return result
    

    
    @api.depends('product_id')
    def _compute_product_uom(self):
        result = super(SaleOrderLine,self)._compute_qty_delivered()
        for line in self:

            if  line.order_id.partner_id.uom_selection == "units" :
                line.product_uom = line.product_id.uom_id
            elif line.order_id.partner_id.uom_selection == "ctn" :
                line.product_uom = line.product_id.secondary_uom_id
        return result