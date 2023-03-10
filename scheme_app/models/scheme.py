# -*- coding: utf-8 -*-
from odoo import api, fields, models,_
from odoo.exceptions import UserError


class Scheme(models.Model):
    _name = "scheme"
    _description = "Scheme Model"

    name = fields.Char(string='Scheme Name')
    currency_id = fields.Many2one('res.currency',string='Currency')
    value = fields.Monetary(string='Value',)
    brand_ids = fields.Many2many('x_product_brand', store=True, string='Brand Name',  readonly=False)
    line_id = fields.One2many('scheme.line', 'scheme_id', string="Scheme Line")
    start_date = fields.Datetime(string='Start Date')
    end_date = fields.Datetime(string='End Date')

    # @api.onchange('brand_ids')
    def onclick_all_brand_line(self):
        order_line=[]
        self['line_id'] = False
        ids =[]
        for brand in self.brand_ids:
            # raise UserError(brand.id)
            # id = str(brand.id).split('_')[1]
            # raise UserError(id)
            ids.append(brand.id)
        
        other_model_record = self.env['product.product'].search([('x_studio_product_brand','in', ids)])
        # raise UserError(other_model_record)
        # raise UserError(other_model_record)
        if other_model_record:
            for rec in other_model_record:
                order_line.append((0,0,{
                    'product_id': rec.id,
                }))
        self['line_id'] = order_line

class SchemeLine(models.Model):
    _name = 'scheme.line'
    _description = "Scheme Line"

    scheme_id = fields.Many2one('scheme')
    type=fields.Selection([('Brand','Brand'),('Product','Product'),('Supplier','Supplier')],string="Type")
    supplier_id=fields.Many2one('res.partner',string="Supplier")
    brand_id=fields.Many2one('x_product_brand',string="Brand")
    product_id = fields.Many2one('product.product',string='Product')
    pcs = fields.Many2one('uom.uom',string='Pcs')
    grams = fields.Char(string='Grams')
    market_commission = fields.Float(string='Market Commission')
    disc = fields.Float(string='Disc %')
    ditributor_commission = fields.Float(string='Ditributor Commission')
    extra_disc = fields.Float(string='Extra Disc %')

class Partner(models.Model):
    _inherit = 'res.partner'
    scheme_id = fields.Many2one('scheme', string="Scheme")
class SaleOrder(models.Model):
    _inherit = 'sale.order'
    scheme_id = fields.Many2one(string="Scheme", related='partner_id.scheme_id')


    @api.onchange('order_line')
    def apply_scheme(self):
        total_discount_mas = 0
        sub_value_1 = 0
        sub_value_2 = 0
        sub_value_3 = 0
        sub_value_4 = 0
        discounted_value_1 = 0
        discounted_value_2 = 0
        discounted_value_3 = 0
        discounted_value_4 = 0
        scheme_line = self.partner_id.scheme_id.line_id
        scheme_main = self.partner_id.scheme_id
        # ('Brand','Brand'),('Product','Product'),('Supplier','Supplier')
        for line in self.order_line:
            for scheme in scheme_line:
                date_strt, date_end =  scheme_main.start_date, scheme_main.end_date
                if date_strt and date_end:
                    if self.date_order >= date_strt and self.date_order <= date_end:
                        if scheme.type == "Product":
                            if line.product_id == scheme.product_id:
                                line['disc_1'] = scheme['market_commission'] 
                                line['disc_2'] = scheme['disc'] 
                                line['disc_3'] = scheme['ditributor_commission'] 
                                line['disc_4'] = scheme['extra_disc']
                        elif scheme.type == "Brand":
                            if line.product_id.x_studio_product_brand == scheme.product_id:
                                line['disc_1'] = scheme['market_commission'] 
                                line['disc_2'] = scheme['disc'] 
                                line['disc_3'] = scheme['ditributor_commission'] 
                                line['disc_4'] = scheme['extra_disc']
                        # elif scheme.type == "Supplier":
                        #     if line.product_id.x_studio_product_brand == scheme.product_id:
                        #         line['disc_1'] = scheme['market_commission'] 
                        #         line['disc_2'] = scheme['disc'] 
                        #         line['disc_3'] = scheme['ditributor_commission'] 
                        #         line['disc_4'] = scheme['extra_disc']

            # if line['disc_1'] >= 0:
                if line['disc_1'] > 0:
                    discounted_value_1 = (line.price_unit * line['disc_1']) / 100
                sub_value_1 = line.price_unit - discounted_value_1
                # raise UserError(sub_value_1)
            # if line['disc_2'] >= 0:
                if line['disc_2'] > 0:
                    discounted_value_2 = (sub_value_1 * line['disc_2']) / 100
                sub_value_2 = sub_value_1 - discounted_value_2
                # raise UserError(sub_value_2)
            # if line['disc_3'] >= 0:
                if line['disc_3'] > 0:
                    discounted_value_3 = (sub_value_2 * line['disc_3']) / 100
                sub_value_3 = sub_value_2 - discounted_value_3
            # if line['disc_4'] >= 0:
                if line['disc_4'] > 0:
                    discounted_value_4 = (sub_value_3 * line['disc_4']) / 100
                sub_value_4 = sub_value_3 - discounted_value_4
                # raise UserError(sub_value_4)
            # line['total_discount'] =  discounted_value_1 + discounted_value_2 + discounted_value_3 + discounted_value_4 #- line['price_subtotal']
            line['price_subtotal'] = sub_value_4 * line.product_uom_qty
            line['total_discount'] = (line.price_unit * line.product_uom_qty) - line['price_subtotal']
        #     total_discount_mas += line['total_discount']
        # self['ks_amount_discount'] = total_discount_mas 
        


class SaleOrderLine(models.Model):
    _inherit = 'sale.order.line'
    disc_1 = fields.Float(string="Discount 1")
    disc_2 = fields.Float(string="Discount 2")
    disc_3 = fields.Float(string="Discount 3")
    disc_4 = fields.Float(string="Discount 4")
    total_discount = fields.Float(string="Total Discount")
