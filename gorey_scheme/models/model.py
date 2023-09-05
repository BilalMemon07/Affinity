from odoo import fields, models, api,_
from odoo.exceptions import UserError
from datetime import datetime,date

class SchemeModel(models.Model):
    _name = "scheme.model"
    _description = "Scheme Model"
    
    name = fields.Char(string='Name',required=True)
    currency_id = fields.Many2one('res.currency',string='Currency')
    value = fields.Float(string='Value')
    start_date = fields.Date(string='Start Date')
    end = fields.Date(string='End Date')
    line_ids = fields.One2many("scheme.model.line", "scheme_id", string="Scheme Lines")

class ResPartnerInherit(models.Model):
    _inherit = 'res.partner'

    customer_scheme_id = fields.Many2one('scheme.model',string='Scheme')
    customer_tax = fields.Boolean(string='With Tax')


class SchemeModelLines(models.Model):
   _name = "scheme.model.line"
   _description = "Scheme Lines"

   scheme_id = fields.Many2one('scheme.model',string='scheme')
   product_id = fields.Many2one('product.product',string='Product')
   market_com = fields.Float(string='Market Com.')
   disc = fields.Float(string='Disc %')
   distributor_com = fields.Float(string='Distributor Com')
   extra_disc = fields.Float(string='Extra Disc')
   



# for rec in self:
#   # rec['x_studio_total_discount'] = 0
#   # if rec.x_studio_total_discount == 0:
#   if rec.move_id.move_type == 'out_invoice':
#     if rec.move_id.move_type:    
    
#       if rec.product_id:
#         disc_amount1 = 0
#         disc_amount2 = 0
#         disc_amount3 = 0
#         if rec.x_studio_discount:
#           disc1 =  rec.x_studio_discount / 100
#           if rec.move_id.move_type == 'out_invoice' and rec.move_id.journal_id.id == 107:
#             disc_amount1 = (rec.price_subtotal-rec.x_studio_sch_value_1) * disc1
#           else:
#             disc_amount1 = (rec.price_total-rec.x_studio_sch_value_1) * disc1
          
#         if rec.x_studio_discount1:
#           disc2 =  rec.x_studio_discount1 / 100
#           if rec.move_id.move_type == 'out_invoice' and rec.move_id.journal_id.id == 107:
#             disc_amount2 = (rec.price_subtotal-rec.x_studio_sch_value_1-disc_amount1) * disc2
#           else:
#             disc_amount2 = (rec.price_total-rec.x_studio_sch_value_1-disc_amount1) * disc2
          
#         if rec.x_studio_discount2:
#           disc3 =  rec.x_studio_discount2 / 100
#           if rec.move_id.move_type == 'out_invoice' and rec.move_id.journal_id.id == 107:
#             disc_amount3 = (rec.price_subtotal-rec.x_studio_sch_value_1-disc_amount1-disc_amount2) * disc3
#           else:
#             disc_amount3 = (rec.price_total-rec.x_studio_sch_value_1-disc_amount1-disc_amount2) * disc3
            
#         subtotal = disc_amount1 + disc_amount2 + disc_amount3
#         if rec.move_id.move_type == 'out_invoice' and rec.move_id.journal_id.id == 107:
#           # if rec.x_studio_total_discount == 0:
#           rec['x_studio_total_discount'] = disc_amount1 + disc_amount2 + disc_amount3
#           # rec['x_studio_total_discount'] = subtotal
#           rec['x_studio_subtotal'] = rec.price_subtotal- subtotal
#         else:
#           rec['x_studio_total_discount'] = subtotal
#           rec['x_studio_subtotal'] = rec.price_total- subtotal
#         # else:
#         #   rec['x_studio_total_discount'] = 0

# sale Order
# for rec in self:
#   rec['x_studio_total_discount'] = 0
#   if rec.product_id:
#     disc_amount1 = 0
#     disc_amount2 = 0
#     disc_amount3 = 0
#     if rec.x_studio_discount_1:
#       disc1 =  rec.x_studio_discount_1 / 100
#       disc_amount1 = (rec.price_total-rec.x_studio_sch_value) * disc1
      
#     if rec.x_studio_discount1:
#       disc2 =  rec.x_studio_discount1 / 100
#       disc_amount2 = (rec.price_total-rec.x_studio_sch_value-disc_amount1) * disc2
      
#     if rec.x_studio_discount2:
#       disc3 =  rec.x_studio_discount2 / 100
#       disc_amount3 = (rec.price_total-rec.x_studio_sch_value-disc_amount1-disc_amount2) * disc3
#     subtotal = disc_amount1 + disc_amount2 + disc_amount3  
#     rec['x_studio_total_discount'] = disc_amount1 + disc_amount2 + disc_amount3
#     rec['x_studio_subtotal'] = rec.price_total- subtotal
#   else:
#     rec['x_studio_total_discount'] = 0