from odoo import fields, models, api,_ ,Command
from odoo.exceptions import UserError
from datetime import datetime,date
from odoo.addons.account.models.account_move_line import AccountMoveLine as AML



class InvoicesInherit(models.Model):
    _inherit = 'account.move'

    invoice_scheme_id = fields.Many2one('scheme.model',string='Scheme',related='partner_id.customer_scheme_id',readonly=True)
    
    market_com = fields.Float(string='Market Comission')
    disc = fields.Float(string='Discount')
    distributor_com = fields.Float(string='Distributor Comission')
    extra_disc = fields.Float(string='Extra Discount')
    total_disc = fields.Float(string='Total Discount')

     

    # bilal 
    untaxed_amount_before_discount = fields.Float(string="Untaxed Amount Before Discount")  
    discount = fields.Float(string="Discount")  
    untaxed_amount_after_discount = fields.Float(string="Untaxed Amount After Discount")  
    tax_amount = fields.Float(string="Tax amount")
    amount_after_discount = fields.Float(string="Amount After Discount")
    custom_tax = fields.Float(string="Custom Tax")
    further_custom_tax = fields.Float(string="further Custom Tax")
    total_custom_tax = fields.Float(string="Total Custom Tax")

    # @api.onchange("invoice_line_ids")
    def apply_scheme_calculation(self):
        for rec in self:
            # raise UserError("Hello")
            total_discount = 0
            untaxed_amount_before_discount = 0
            toatal_tax = 0
            for line in rec.invoice_line_ids:
                if line.total_disc:
                    total_discount += line.total_disc
                if line.with_o_tax:
                    untaxed_amount_before_discount += line.with_o_tax
                if untaxed_amount_before_discount:
                    for tax in line.tax_ids:
                        toatal_tax += line.with_o_tax * ((tax.amount / 100) + 1)
                

            rec['untaxed_amount_before_discount'] = untaxed_amount_before_discount
            rec['discount'] = total_discount
            rec['untaxed_amount_after_discount'] = untaxed_amount_before_discount - total_discount
            rec['tax_amount'] = toatal_tax
            rec['amount_after_discount'] = rec.untaxed_amount_after_discount + rec.tax_amount

            rec.calculate_custom_tax()


    def calculate_custom_tax(self):
        for rec in self:
            res = {}
            total_further_tax = 0
            total_tax_amount = 0
            for line in rec.invoice_line_ids:
                # res = line.calculate_tax_amount()
                # raise UserError(str(res))
                subtotal = line.price_subtotal - line['total_disc']
                for tax in line.tax_ids:
                    if not tax.tax_group_id.is_further_tax:
                        total_tax_amount = total_tax_amount + (((subtotal) * tax.amount)/100)
                    elif tax.tax_group_id.is_further_tax:
                        total_further_tax = total_further_tax + (((subtotal) * tax.amount)/100)
            rec['custom_tax'] = total_tax_amount
            rec['further_custom_tax'] = total_further_tax
            rec['total_custom_tax'] = rec.custom_tax + rec.further_custom_tax

            # rec['market_com'] = res['market_com']  
            # rec['disc'] = res['disc']
            # rec['distributor_com'] = res['distributor_com']
            # rec['extra_disc'] = res['extra_disc']
            

   
                           



   

    @api.onchange("invoice_line_ids")
    def apply_computattion(self):
        self.apply_scheme_calculation()
            # self.compute_discount_on_journel_items()

    # AML._prepare_exchange_difference_move_vals = _prepare_exchange_difference_move_vals

    def call_all_functions(self):
        self.apply_scheme_calculation()

class InvoicesLineInherit(models.Model):
    _inherit='account.move.line'

    market_com = fields.Float(string='Market Comission')
    disc = fields.Float(string='Discount')
    distributor_com = fields.Float(string='Distributor Comission')
    extra_disc = fields.Float(string='Extra Discount')
    total_disc = fields.Float(string='Total Discount')

    # bilal
    with_tax = fields.Float(string="With Tax")
    with_o_tax = fields.Float(string="Without Tax")
    tax_amount = fields.Float(string="Tax Amount")


    # def create_discount_lines(self):




    def compute_total(self):    
        for rec in self:  
            scheme_data = rec.move_id.invoice_scheme_id
            order_date = rec.move_id.invoice_date
            if rec.move_id.invoice_scheme_id:
                # if scheme_data.start_date <= order_date <= scheme_data.end:
                for sch_line in scheme_data.line_ids:
                    if rec.product_id == sch_line.product_id:
                        rec['market_com'] = sch_line.market_com
                        rec['disc'] = sch_line.disc
                        rec['distributor_com'] = sch_line.distributor_com
                        rec['extra_disc'] = sch_line.extra_disc
                                    
                # else:
                #     raise UserError("Scheme Expired ! Please update your date")

    def calculate_tax_amount(self):
        for rec in self:
            total_tax = 0
            res = {}
            if rec.move_id.partner_id.customer_tax and rec.tax_ids:
                if rec.tax_ids:
                    for tax in rec.tax_ids:
                        total_tax += tax.amount
                    
                    if rec.quantity and rec.price_unit:
                        rec['with_tax'] = rec.quantity * rec.price_unit
                        if rec.with_tax:
                            rec['with_o_tax'] = rec.with_tax / ((total_tax / 100) + 1)
                            rec.apply_scheme(rec['with_o_tax'])
                            if rec.with_o_tax:
                                rec['tax_amount'] =  rec.with_o_tax * ((total_tax / 100))
            else:
                rec.apply_scheme(rec.quantity * rec.price_unit)

            # return res

    @api.onchange('product_id','quantity','price_unit','tax_ids')
    def onchange_line_items(self):
        self.compute_total()
        self.calculate_tax_amount()
        
    def call_all_functions(self):
        self.compute_total()
        self.calculate_tax_amount()

  
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
        for line in self:                           
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


    




   
   
class TaxGroup(models.Model):
    _inherit = "account.tax.group" 

    is_further_tax = fields.Boolean(string="Is Further Tax")

