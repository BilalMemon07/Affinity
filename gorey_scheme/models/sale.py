from odoo import fields, models, api,_
from odoo.exceptions import UserError
from datetime import datetime,date


class SaleOrderInherit(models.Model):
    _inherit = 'sale.order'

    sale_scheme_id = fields.Many2one('scheme.model',string='Scheme',related='partner_id.customer_scheme_id',readonly=True)
    total_discount = fields.Float(string = "Total Discount")
    
    
    @api.onchange("order_line")
    def compute_total(self):    
        for rec in self:  
            scheme_data = rec.sale_scheme_id
            order_date = rec.date_order.date()
            if rec.sale_scheme_id:
                # if scheme_data.start_date <= order_date <= scheme_data.end:
                for line in rec.order_line:
                        for sch_line in scheme_data.line_ids:
                            if line.product_id == sch_line.product_id:
                                line['market_com'] = sch_line.market_com
                                line['disc'] = sch_line.disc
                                line['distributor_com'] = sch_line.distributor_com
                                line['extra_disc'] = sch_line.extra_disc
                                    
                # else:
                #     raise UserError("Scheme Expired ! Please update your date")
        
        rec.calculate_tax_amount()

    def calculate_tax_amount(self):
        for rec in self:
            total_tax = 0
            res = {}
            for line in rec.order_line:
                if rec.partner_id.customer_tax and line.tax_id:
                    with_tax = 0
                    with_o_tax = 0
                    tax_amount = 0
                    if line.tax_id:
                        for tax in line.tax_id:
                            total_tax += tax.amount
                        
                        if line.product_uom_qty and line.price_unit:
                            with_tax += line.product_uom_qty * line.price_unit
                            if with_tax:
                                with_o_tax += with_tax / ((total_tax / 100) + 1)
                                rec.apply_scheme(with_o_tax)
                                if with_o_tax:
                                    tax_amount +=  with_o_tax * ((total_tax / 100))
                else:
                    rec.apply_scheme(line.product_uom_qty * line.price_unit)

    # def apply_scheme(self):
    #     total_discount_mas = 0
    #     sub_value_1 = 0
    #     sub_value_2 = 0
    #     sub_value_3 = 0
    #     sub_value_4 = 0
    #     discounted_value_1 = 0
    #     discounted_value_2 = 0
    #     discounted_value_3 = 0
    #     discounted_value_4 = 0
    #     total_discount = 0
    #     if self.partner_id.customer_scheme_id:
    #         for line in self.order_line:                           
            
    #             if line['market_com'] > 0:
    #                 discounted_value_1 = (line.price_unit * line['market_com']) / 100
    #             sub_value_1 = line.price_unit - discounted_value_1
                
    #             if line['disc'] > 0:
    #                 discounted_value_2 = (sub_value_1 * line['disc']) / 100
    #             sub_value_2 = sub_value_1 - discounted_value_2
              
    #             if line['distributor_com'] > 0:
    #                 discounted_value_3 = (sub_value_2 * line['distributor_com']) / 100
    #             sub_value_3 = sub_value_2 - discounted_value_3
            
    #             if line['extra_disc'] > 0:
    #                 discounted_value_4 = (sub_value_3 * line['extra_disc']) / 100
    #             sub_value_4 = sub_value_3 - discounted_value_4
              
    #             line['price_subtotal'] = sub_value_4 * line.product_uom_qty
    #             line['total_disc'] = (line.price_unit * line.product_uom_qty) - line['price_subtotal']
    #             total_discount += line.total_disc
    #     self['total_discount'] = total_discount 



    def apply_scheme(self, amount):

        sub_value_1 = 0
        sub_value_2 = 0
        sub_value_3 = 0
        sub_value_4 = 0
        discounted_value_1 = 0
        discounted_value_2 = 0
        discounted_value_3 = 0
        discounted_value_4 = 0
        
        subtotal =0
        total_discount = 0
        for line in self.order_line:                           
            if line['market_com'] > 0:
                discounted_value_1 = (amount * line['market_com']) / 100
            sub_value_1 = amount - discounted_value_1
            if line['disc'] > 0:
                discounted_value_2 = (sub_value_1 * line['disc']) / 100
            sub_value_2 = sub_value_1 - discounted_value_2
            
            if line['distributor_com'] > 0:
                discounted_value_3 = (sub_value_2 * line['distributor_com']) / 100
            sub_value_3 = sub_value_2 - discounted_value_3
        
            if line['extra_disc'] > 0:
                discounted_value_4 = (sub_value_3 * line['extra_disc']) / 100
            sub_value_4 = sub_value_3 - discounted_value_4
            
            
            line['total_disc'] =  discounted_value_1 + discounted_value_2 + discounted_value_3 + discounted_value_4
            total_discount += line.total_disc
        self['total_discount'] = total_discount 

class SaleOrderLineInherit(models.Model):
    _inherit='sale.order.line'

    market_com = fields.Float(string='Market Comission')
    disc = fields.Float(string='Discount')
    distributor_com = fields.Float(string='Distributor Comission')
    extra_disc = fields.Float(string='Extra Discount')
    total_disc = fields.Float(string='Total Discount')