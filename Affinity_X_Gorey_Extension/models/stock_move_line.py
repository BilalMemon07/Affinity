# -*- coding: utf-8 -*-

from odoo import models, fields, api
from odoo.exceptions import UserError


class StockMoveLine(models.Model):
    _inherit = 'stock.move.line'
    

    done_in_ctn = fields.Float(string="Done In CTN",store=True)
    reserved_in_ctn = fields.Float(string="Reserved in CTN",store=True)
    operation_type_code = fields.Selection(related='picking_id.picking_type_id.code')

    

    @api.onchange("done_in_ctn")
    def compute_done_in_ctn(self):
        for rec in self:
            if rec.picking_id.picking_type_id.code == "outgoing":
                qty = rec.done_in_ctn * rec.product_id.product_tmpl_id.secondary_uom_id.factor_inv
                rec['qty_done'] = qty
    

    @api.depends('product_uom_id.category_id', 'product_id.uom_id.category_id', 'move_id.product_uom', 'product_id.uom_id')
    def _compute_product_uom_id(self):
        result = super(StockMoveLine,self)._compute_product_uom_id()
        for line in self:
            if line.picking_id.picking_type_id.code == "internal":
                line.product_uom_id = line.product_id.secondary_uom_id.id
        return result
    
    @api.depends('product_id', 'product_uom_id', 'reserved_uom_qty')
    def _compute_reserved_qty(self):
        result = super(StockMoveLine,self)._compute_reserved_qty()
        for line in self:
            line.reserved_qty = line.product_uom_id._compute_quantity(line.reserved_uom_qty, line.product_id.uom_id, rounding_method='HALF-UP')
            qty = line.reserved_uom_qty / line.product_id.product_tmpl_id.secondary_uom_id.factor_inv
            line['reserved_in_ctn'] = qty
        return result



    
 

                