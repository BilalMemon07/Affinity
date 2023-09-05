# -*- coding: utf-8 -*-

from odoo import models, fields, api
from odoo.exceptions import UserError
from odoo.tools import config, human_size, ImageProcess, str2bool, consteq
import base64


UOM = [
    ('units', 'Units'),
    ('ctn', 'CTN'),
]
class ProductTemplate(models.Model):
    _inherit = 'product.template'


    secondary_uom_id = fields.Many2one('uom.uom', string="secondary UoM")

class ProductPriceListItem(models.Model):
    _inherit = 'product.pricelist.item'



    ctn_price = fields.Float(string="CTN Price")

    @api.onchange("product_tmpl_id","ctn_price")
    def compute_ctn_price(self):
        for line in self:
            # raise UserError("price")
            if line.ctn_price and line.product_tmpl_id:
                price = line.ctn_price / line.product_tmpl_id.secondary_uom_id.factor_inv
                line['fixed_price'] = price



class Partner(models.Model):
    _inherit = 'res.partner'

    uom_selection = fields.Selection(selection=UOM, string=" Uom Selection",store=True)