# -*- coding: utf-8 -*-

from odoo import models, fields, api
from odoo.exceptions import UserError
from odoo.tools import config, human_size, ImageProcess, str2bool, consteq
import base64


class Finance(models.Model):
    _name = 'finance.model'
    _description = "Finance Plan"

    name = fields.Char(string="Name", store=True)
    from_date = fields.Date(string="From Date",store=True)
    due_date  =  fields.Date(string="To Date", store=True)
    line_ids = fields.One2many("finance.line.model", "finance_id", string="Line Items", store=True)


    def apply_finance_plan (self):
        line_ids_list = []
        line_disct = {}
        for rec in self:
            if rec.from_date and rec.due_date:
                price_unit = 0
                product_qty = 0
                skua = 0
                purchase_order  = self.env['purchase.order'].search([])
                for po in purchase_order:
                    
                    # for po_i in range(len(purchase_order[po].order_line)):
                    #     for po_j in range(po_i + 1, len(purchase_order[po].order_line)):
                    #         if purchase_order[po].order_line[po_i].product_id.categ_id.id == purchase_order[po].order_line[po_j].product_id.categ_id.id:
                    #             if po == 2:
                    #                 raise UserError('po2')
                    #             price_unit  += purchase_order[po].order_line[po_i].price_unit + purchase_order[po].order_line[po_j].price_unit
                    #             product_qty += purchase_order[po].order_line[po_i].product_qty + purchase_order[po].order_line[po_j].product_qty
                                
                    #             # skua += po.order_line[po_i] + po.order_line[po_j]
                    #             # raise UserError("Hello")
                    #             obj = {
                    #                 "po_number": purchase_order[po].name,
                    #                 "supplier_id": purchase_order[po].partner_id.id,
                    #                 "currency_id" :purchase_order[po].currency_id.id,
                    #                 "uom_id" : purchase_order[po].order_line[po_j].product_uom.id,
                    #                 "category_id": purchase_order[po].order_line[po_j].product_id.categ_id.id,
                    #                 "unit_price":price_unit,
                    #                 "qty":product_qty,
                    #                 "skua" : skua,
                    #                 "finance_id" :rec.id
                    #             }
                    

                    for line in po.order_line:
                        if line.product_id.categ_id.id not in line_disct:
                                line_disct[str(line.product_id.categ_id.id) +'_'+ str(po.name)] = {
                                    "po_number": po.name,
                                    "po_number": po.name,
                                    "supplier_id": po.partner_id.id,
                                    "currency_id" :po.currency_id.id,
                                    "uom_id" : line.product_uom.id,
                                    "category_id": line.product_id.categ_id.id,
                                    "unit_price": line.price_unit,
                                    "qty":line.product_qty,
                                    # "skua" : skua,
                                    "finance_id" :rec.id
                                }


                        else:
                            # if line_disct[line.product_id.categ_id.id]['po_number'] == po.name: 
                            line_disct[str(line.product_id.categ_id.id) +'_'+ str(po.name)]['unit_price'] += line.price_unit
                            line_disct[str(line.product_id.categ_id.id) +'_'+ str(po.name)]['qty'] += line.product_qty
                            # else:
                            #     line_disct[line.product_id.categ_id.id] = {
                            #         "po_number": po.name,
                            #         "supplier_id": po.partner_id.id,
                            #         "currency_id" :po.currency_id.id,
                            #         "uom_id" : line.product_uom.id,
                            #         "category_id": line.product_id.categ_id.id,
                            #         "unit_price": line.price_unit,
                            #         "qty":line.product_qty,
                            #         # "skua" : skua,
                            #         "finance_id" :rec.id
                            #     }
                            
                for dis in line_disct:
                    line_ids_list.append((0,0,line_disct[dis]))
                    
                self.write({
                    'line_ids':line_ids_list
                })


    

class FinanceLine(models.Model):
    _name = 'finance.line.model'
    _description = "Finance line Plan"  


    finance_id = fields.Many2one("finance.model", string="Finance", store=True)
    batch = fields.Char(string="Batch")
    po_number = fields.Char(string="Refrence")
    description = fields.Char(string="Description")
    uom_id = fields.Many2one('uom.uom', string="Unit")
    skua = fields.Integer(string='SKUA')
    category_id = fields.Many2one('product.category' , string="Category")
    supplier_id = fields.Many2one('res.partner', string="Supplier")
    lead_time_weeks = fields.Float(string="Lead Time (Weeks)")
    currency_id = fields.Many2one('res.currency',string="Currency")
    unit_price = fields.Float(string="Unit Price")   
    price_in_usd = fields.Float(string="Price in USD")
    percentage = fields.Integer(string="Percentage")
    tax_rate = fields.Integer(string="Tax Rate (Custom Duty / Landed Cost) HS Code Depnded")
    qty = fields.Float(string=" Qty")
    gross_amount = fields.Float(string="Gross Amount")
    expected_payment_date = fields.Date(string="Expected Payment Date")
    payment_amount = fields.Float(string="Payment Amount")
    head_of_payment = fields.Float(string="Head of Payment")
    sub_header = fields.Selection(selection=[('balance_payment','Balance Payment'), ('advance_payment','Advance Payment'), ('material_payment','Material Payment')])
    journal_id = fields.Many2one('account.journal', string='Journal',domain = [('type','in',('bank','cash'))] )
    payment_mode = fields.Many2one('payment.mode', string="Payment Mode")
    month = fields.Integer(string="Month")
    week = fields.Integer(string="Week")
    country_id = fields.Many2one('res.country', string="Country")
    remarks = fields.Text(string="Remarks")


class ModeOFPayment(models.Model):
    _name = "payment.mode"
    _description = "Mode of Payment"


    name = fields.Char(string="Payment Mode Name") 
