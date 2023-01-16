# -*- coding: utf-8 -*-
from odoo import api, fields, models,_
from odoo.exceptions import UserError


class GateModule(models.Model):
    _name = "scheme"
    _description = "Scheme Model"

    name = fields.Char(string='Scheme Name')
    currency_id = fields.Many2one('res.currency',string='Currency')
    value = fields.Monetary(string='Value',)
    line_id = fields.One2many('scheme.line', 'scheme_id', string="Expense Line")

class ExpenseLine(models.Model):
    _name = 'scheme.line'
    _description = "Scheme Line"

    scheme_id = fields.Many2one('scheme')
    product_id = fields.Many2one('product.product',string='Product')
    start_date = fields.Date(string='Start Date')
    end_date = fields.Date(string='End Date')
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
        sub_value_1 = 0
        sub_value_2 = 0
        sub_value_3 = 0
        sub_value_4 = 0
        discounted_value_1 = 0
        discounted_value_2 = 0
        discounted_value_3 = 0
        discounted_value_4 = 0
        scheme_line = self.partner_id.scheme_id.line_id
        for line in self.order_line:
            for scheme in scheme_line:
                if line.product_id == scheme.product_id:
                    line['disc_1'] = scheme['market_commission'] 
                    line['disc_2'] = scheme['disc'] 
                    line['disc_3'] = scheme['ditributor_commission'] 
                    line['disc_4'] = scheme['extra_disc']
            if line['disc_1'] != 0:
                discounted_value_1 = (line.price_unit * line['disc_1']) / 100
                sub_value_1 = line.price_unit - discounted_value_1
            if line['disc_2'] != 0:
                discounted_value_2 = (sub_value_1 * line['disc_2']) / 100
                sub_value_2 = sub_value_1 - discounted_value_2
            if line['disc_3'] != 0:
                discounted_value_3 = (sub_value_2 * line['disc_3']) / 100
                sub_value_3 = sub_value_2 - discounted_value_3
            if line['disc_4'] != 0:
                discounted_value_4 = (sub_value_3 * line['disc_4']) / 100
                sub_value_4 = sub_value_3 - discounted_value_4
                # raise UserError(sub_value_4)
            if discounted_value_4 >= 0:
                line['total_discount'] = sub_value_4

class SaleOrderLine(models.Model):
    _inherit = 'sale.order.line'
    disc_1 = fields.Float(string="Discount 1")
    disc_2 = fields.Float(string="Discount 2")
    disc_3 = fields.Float(string="Discount 3")
    disc_4 = fields.Float(string="Discount 4")
    total_discount = fields.Float(string="Total Discount")
