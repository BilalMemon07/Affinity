# -*- coding: utf-8 -*-
# Copyright (C) Softhealer Technologies.
from odoo import fields,models,api,_
import requests
import json
import traceback
from odoo.exceptions import UserError
import qrcode
import base64
import io
import datetime

class Product(models.Model):
    _inherit = 'product.template'

    pct_code = fields.Char("PCT Code")

class PosConfig(models.Model):
    _inherit = 'pos.config'

    pos_id = fields.Char("POSID",required=1)
    fbr_authorization = fields.Char("FBR Header Authorization")

class r_partner(models.Model):
    _inherit = 'res.partner'
    
    cnic = fields.Char(string='CNIC')

class POSOrder(models.Model):
    _inherit = 'pos.order'
    
    fbr_respone = fields.Text("FBR Response")
    post_data_fbr = fields.Boolean("Post Data Successful ?")
    pos_reference = fields.Char(string='Receipt Ref', readonly=True, copy=True)
    invoice_number = fields.Char("Invoice Number")
                
    #Asir
    def post_data_to_order(self, ref, invoice_numberJS, responseJS):
        if self.company_id.id != 2:
            posOrder = self.env['pos.order'].search([('pos_reference', '=', ref)])
            if posOrder:
                posOrder.post_data_fbr = True
                posOrder.invoice_number = invoice_numberJS
                posOrder.fbr_respone = responseJS
                img = qrcode.make(invoice_numberJS)
                result = io.BytesIO()
                img.save(result, format='PNG')
                result.seek(0)
                img_bytes = result.read()
                base64_encoded_result_bytes = base64.b64encode(img_bytes)
                return [posOrder.config_id.pos_id,base64_encoded_result_bytes.decode('ascii')]

    #Asir
    def get_fbr_pos_id(self, ref, invoice_numberJS, responseJS):
        if self.company_id.id != 2:
            posOrder = self.env['pos.order'].search([('pos_reference', '=', ref)])
            if posOrder:
                fbr_pos_id = posOrder.x_studio_fbr_pos_id
                # fbr_pos_company = posOrder.x_studio_fbr_pos_company
                return fbr_pos_id


    
    def post_data_fbi(self, pos_order_data):
        if self.company_id.id != 2:
            fbr_url = "https://esp.fbr.gov.pk:8244/FBR/v1/api/Live/PostData" #sandbox
            # fbr_url = "https://gw.fbr.gov.pk/imsp/v1/api/Live/PostData"
            #Content type must be included in the header
            header = {"Content-Type": "application/json"}
            invoice_number = ''
            r_ref = ''
            amount = 0.0
            tax = 0.0
            if pos_order_data :
                try:
                    payment_lines = 0
                    
                    for pos_order in pos_order_data:
                        #Asir getting fbr fees amount
                        fbrAmount = 0
                        for line in pos_order.get('lines'):
                            product_dic = line[2]
                            #Asir change product id here for FBR Product
                            if product_dic.get('product_id') == 10283:
                                fbrAmount = product_dic.get('price_subtotal')
                                break
                        # order_uid = pos_order.get('uid')
                        # order = self.env['pos.order'].search([('pos_reference','ilike',order_uid)])
                        # if order:
                            # return
                        amount = (pos_order.get('amount_total') if pos_order.get('amount_total') > 0 else  (pos_order.get('amount_total') * -1)) 
                        tax = (pos_order.get('amount_tax') if pos_order.get('amount_tax') > 0 else  (pos_order.get('amount_tax') * -1)) 
                        amount = amount - fbrAmount #Asir FBR amount removal
                        order_session_id = self.env['pos.session'].search([('id','=',pos_order.get('pos_session_id'))])
                        order_dic = {
                                        "InvoiceNumber": "",
                                        "POSID": order_session_id.config_id.pos_id,
                                        "USIN": pos_order.get('uid'),
                                        "RefUSIN": "",
                                        "DateTime": fields.Datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                                        "TotalBillAmount": amount, #pos_order.get('amount_total'),
                                        "TotalSaleValue": amount - tax, #pos_order.get('amount_total') - pos_order.get('amount_tax'),
                                        "TotalTaxCharged": tax, #pos_order.get('amount_tax'),
                                        "PaymentMode": 1,
                                        "InvoiceType": 1,
                                }
                        
                        r_ref = pos_order.get('return_ref')
                        if r_ref:
                            order_dic.update({"RefUSIN": r_ref,
                            })
                            amount = pos_order.get('amount_total')
                            if amount > 0:
                                order_dic.update({"InvoiceType": 2, #Debit
                                })
                            if amount < 0:
                                order_dic.update({"InvoiceType": 3, #Credit
                                })
                        
                        payment_lines = pos_order.get("statement_ids")
                        pay_lines = len(payment_lines)
                        if pay_lines > 1:
                            order_dic.update({"PaymentMode": 5, #Mixed
                            })
                    
                        if pay_lines == 1:
                            pl_v1 = payment_lines[0]
                            pl_v2 = pl_v1[2]
                            pl_v3 = pl_v2['payment_method_id']
                            
                            if pl_v3 == 1:
                                order_dic.update ({"PaymentMode": 1, #Cash
                                })
                            
                            if (pl_v3 == 3) or (pl_v3 == 4) or (pl_v3 == 5) or (pl_v3 == 9):
                                order_dic.update ({"PaymentMode": 2, #Card
                                })                    
                        
                        
                        session = self.env['pos.session'].sudo().search([('id','=',pos_order.get('pos_session_id'))])
                        if session:
                            #header.update({'Authorization': session.config_id.fbr_authorization})
                            header.update({'Authorization': 'Bearer 1298b5eb-b252-3d97-8622-a4a69d5bf818'}) #sandbox
                        
                        
                        if pos_order.get('partner_id'):
                            partner = self.env['res.partner'].sudo().search([('id','=',pos_order.get('partner_id'))])
                            order_dic.update({
                                "BuyerName": partner.name,
                                "BuyerPhoneNumber": partner.mobile,
                                "BuyerNTN": partner.vat,
                                })
                        
                        if pos_order.get('lines'):
                            
                            items_list = []
                            total_qty = 0.0
                            l_qty = 0.0
                            p_stotal = 0.0
                            p_stotal_inc = 0.0
                                
                            for line in pos_order.get('lines'):
                                product_dic = line[2]
                                #Asir FBR Fees check change ID here
                                if product_dic.get('product_id') != 10283:
                                    p_stotal = (product_dic.get('price_subtotal') if product_dic.get('price_subtotal') > 0 else (product_dic.get('price_subtotal') * -1))
                                    p_stotal_inc = (product_dic.get('price_subtotal_incl') if product_dic.get('price_subtotal_incl') > 0 else (product_dic.get('price_subtotal_incl') * -1))
                                    
                                    l_qty = (product_dic.get('qty') if product_dic.get('qty') > 0 else (product_dic.get('qty') * -1))
                                    total_qty += l_qty #product_dic.get('qty')
                                    
                                    if 'product_id' in product_dic:
                                        product = self.env['product.product'].sudo().search([('id','=',product_dic.get('product_id'))])
                                        price_unit = (product_dic.get('price_unit') * 100) / 112
                                        if product:
                                            disc_amt = ((product_dic.get('price_unit')) * (product_dic.get('discount')/100))
                                            if product_dic.get('price_subtotal') >= 0:
                                                line_dic = {
                                                        "ItemCode": product.default_code,
                                                        # "ItemName": product.x_studio_vname + " - " + product.barcode,
                                                        "ItemName": product.name + " - " + product.barcode,
                                                        "Quantity": (product_dic.get('qty')), #product_dic.get('qty'),
                                                        "PCTCode": product.pct_code,
                                                        "TaxRate": 12.0,
                                                        "SaleValue": product_dic.get('price_subtotal'),
                                                        "TotalAmount": product_dic.get('price_subtotal_incl'),
                                                        "TaxCharged": product_dic.get('price_subtotal_incl') - product_dic.get('price_subtotal'), 
                                                        "InvoiceType": 1,
                                                        "RefUSIN": "",
                                                        "Discount": ((product_dic.get('price_unit')) * (product_dic.get('discount')/100))
                                                    }
                                            else:
                                                line_dic = {
                                                        "ItemCode": product.default_code,
                                                        # "ItemName": product.x_studio_vname + " - " + product.barcode,
                                                        "ItemName": product.name + " - " + product.barcode,
                                                        "Quantity": (product_dic.get('qty'))*-1, #product_dic.get('qty'),
                                                        "PCTCode": product.pct_code,
                                                        "TaxRate": 12.0,
                                                        "SaleValue": product_dic.get('price_subtotal')*-1,
                                                        "TotalAmount": product_dic.get('price_subtotal_incl')*-1,
                                                        "TaxCharged": (product_dic.get('price_subtotal_incl') - product_dic.get('price_subtotal'))*-1, 
                                                        "InvoiceType": 3,
                                                        "RefUSIN": "",
                                                        "Discount": ((product_dic.get('price_unit')) * (product_dic.get('discount')/100))
                                                    }                            
                                            if r_ref:
                                                line_dic.update({"RefUSIN": r_ref,
                                                })
                                                amount = pos_order.get('amount_total')
                                                if amount > 0:
                                                    line_dic.update({"InvoiceType": 2, #Debit
                                                    })
                                                if amount < 0:
                                                    line_dic.update({"InvoiceType": 3, #Credit
                                                    })
                                            
                                            items_list.append(line_dic)
                            order_dic.update({'Items':items_list,'TotalQuantity':total_qty})

                        # raise UserError(str(order_dic))
                        # return json.dumps(order_dic)
                        payment_response = requests.post(fbr_url,data=json.dumps(order_dic), headers=header, verify=False, timeout=200)
                        r_json=payment_response.json()
                        invoice_number = r_json.get('InvoiceNumber')
                        # if invoice_number:
                        #     global fbrInvoiceNumber
                        #     fbrInvoiceNumber = invoice_number
                        
                        
                        # values = pos_order.get('statement_ids')
                        # values1 = values[0]
                        # values2 = values1[2]
                        # values3 = values2['payment_method_id']
                        #r_json
                        values = r_json
                    
                except Exception as e:
                    values = dict(
                                exception=e,
                                traceback=traceback.format_exc(),
                            )
                    return ["",values]
            return [invoice_number,values,order_dic] 
        
  
    # def post_data_to_fbr(self, orders):
    #     fbr_url = "https://esp.fbr.gov.pk:8244/FBR/v1/api/Live/PostData"
    #     # fbr_url = "https://gw.fbr.gov.pk/imsp/v1/api/Live/PostData"
        
    #     #Content type must be included in the header
    #     header = {"Content-Type": "application/json"}
    
  
    def post_data_to_fbr(self, orders):
        if self.company_id.id != 2:

            fbr_url = "https://esp.fbr.gov.pk:8244/FBR/v1/api/Live/PostData" #sandbox
            # fbr_url = "https://gw.fbr.gov.pk/imsp/v1/api/Live/PostData"
            
            #Content type must be included in the header
            header = {"Content-Type": "application/json"}

            # raise UserError(str(len(orders)))
            for order in orders:
                order = self.browse(order)
                try:
                    if order and order.session_id and order.session_id.config_id and order.session_id.config_id.fbr_authorization:
                        #header.update({'Authorization': order.session_id.config_id.fbr_authorization})
                        header.update({'Authorization': 'Bearer 1298b5eb-b252-3d97-8622-a4a69d5bf818'})   #sandbox
                        
                        #Asir FBR Fees working
                        fbrAmount = 0
                        for line in order.lines:
                            #Asir change product ID here for FBR Product
                            if line.product_id.id == 10283:
                                fbrAmount = line.price_subtotal
                                break

                        amount_total = order.amount_total
                        amount_total = amount_total - fbrAmount #Asir FBR Fees Removal
                        bill_amount = amount_total
                        tax_amount = order.amount_tax
                        sale_amount = amount_total - order.amount_tax
                        posref = str(order.pos_reference).split(' ')[1]
                        #Asir
                        if 'REFUND' in order.name:
                            order_dic = {
                                        "InvoiceNumber": "",
                                        "POSID": order.session_id.config_id.pos_id,
                                        # "USIN": order.pos_reference,
                                        "USIN": posref,
                                        "DateTime": order.date_order.strftime("%Y-%m-%d %H:%M:%S"),
                                        "TotalBillAmount": bill_amount*-1,
                                        "TotalSaleValue": sale_amount*-1,
                                        "TotalTaxCharged": tax_amount*-1,
                                        "PaymentMode": 1,
                                        "InvoiceType": 3,
                                }
                        
                        else:
                            order_dic = {
                                        "InvoiceNumber": "",
                                        "POSID": order.session_id.config_id.pos_id,
                                        # "USIN": order.pos_reference,
                                        "USIN": posref,
                                        "DateTime": order.date_order.strftime("%Y-%m-%d %H:%M:%S"),
                                        "TotalBillAmount": bill_amount,
                                        "TotalSaleValue": sale_amount,
                                        "TotalTaxCharged": tax_amount,
                                        "PaymentMode": 1,
                                        "InvoiceType": 1,
                                }
                        
                        # if order.payment_ids:
                            # if order.payment_ids > 1:
                                # order_dic.update({
                                    # "PaymentMode": 5,
                                    # })
                            
                            # if order.payment_ids == 1:
                                # order_dic.update({
                                    # "PaymentMode": order.payment_ids.payment_method_id,
                                    # })       
                            
                        # if order.partner_id:
                                # order_dic.update({
                                    # "BuyerName": order.partner_id.name,
                                    # "BuyerPhoneNumber": order.partner_id.mobile,
                                    # })
                            
                        if order.lines:
                            items_list = []
                            total_qty = 0.0
                            for line in order.lines:
                                #Asir change product ID here for FBR Product
                                if line.product_id.id != 10283:
                                    total_qty += line.qty
                                    if line.price_subtotal >= 0:
                                        line_dic = {
                                                "ItemCode": line.product_id.default_code,
                                                # "ItemName": line.product_id.x_studio_vname + " - " + line.product_id.barcode,
                                                "ItemName": line.product_id.name + " - " + line.product_id.barcode,
                                                "Quantity": line.qty,
                                                "PCTCode": line.product_id.pct_code,
                                                "TaxRate": 12.0,
                                                "SaleValue": line.price_subtotal,
                                                "TotalAmount": line.price_subtotal_incl,
                                                "TaxCharged": line.price_subtotal_incl - line.price_subtotal,
                                                "InvoiceType": 1,
                                                "RefUSIN": "",
                                                "Discount": line.price_unit * (line.discount/100)
                                            }
                                        items_list.append(line_dic)
                                    else:
                                        line_dic = {
                                                "ItemCode": line.product_id.default_code,
                                                # "ItemName": line.product_id.x_studio_vname + " - " + line.product_id.barcode,
                                                "ItemName": line.product_id.name + " - " + line.product_id.barcode,
                                                "Quantity": line.qty*-1,
                                                "PCTCode": line.product_id.pct_code,
                                                "TaxRate": 12.0,
                                                "SaleValue": line.price_subtotal*-1,
                                                "TotalAmount": line.price_subtotal_incl*-1,
                                                "TaxCharged": (line.price_subtotal_incl - line.price_subtotal)*-1,
                                                "InvoiceType": 3,
                                                "RefUSIN": "",
                                                "Discount": line.price_unit * (line.discount/100)
                                            }
                                        items_list.append(line_dic)
                            
                            #Asir
                            if 'REFUND' in order.name:
                                order_dic.update({
                                    "Items": items_list,
                                    "TotalQuantity":total_qty*-1
                                })
                            else:
                                order_dic.update({
                                    "Items": items_list,
                                    "TotalQuantity":total_qty
                                })
                        payment_response = requests.post(fbr_url,data=json.dumps(order_dic), headers=header, verify=False, timeout=20)
                        r_json=payment_response.json()
                        invoice_number = r_json.get('InvoiceNumber')
                        if 'REFUND' in order.name:
                            order.write({'fbr_respone':r_json,'post_data_fbr':True,'invoice_number':invoice_number, 'x_studio_refunded_order_posted':True})
                        else:
                            order.write({'fbr_respone':r_json,'post_data_fbr':True,'invoice_number':invoice_number})
                except Exception as e:
                    values = dict(
                                exception=e,
                                traceback=traceback.format_exc(),
                            )
                    order.write({'fbr_respone':values})
    
    # #Asir
    # def post_data_to_fbr_cron(self):
    #     failed_orders = self.search([('post_data_fbr','=',False),('x_studio_pos','ilike','DMTR')])
    #     if failed_orders:
    #         for order in failed_orders:
    #             order.post_data_to_fbr_action()
    #     # for failed_orders in self.search([('post_data_fbr','=',False)]):
    #     #     failed_orders.post_data_to_fbr_action()

    #Asir
    def post_data_to_fbr_cron(self):
        if self.company_id.id != 2:
            failed_orders = self.search([('post_data_fbr','=',False)])
            if failed_orders:
                d1 = datetime.datetime(2022, 4, 1)
                for order in failed_orders:
                    if 'REFUND' in order.name and order.date_order >= d1:
                        order.post_data_to_fbr_action()
            # for failed_orders in self.search([('post_data_fbr','=',False)]):
            #     failed_orders.post_data_to_fbr_action()
        
    #Asir
    def post_data_to_fbr_action(self):
        if self.company_id.id != 2:

            orders = []
            for order in self:
                if order.post_data_fbr and order.invoice_number and order.fbr_respone and not 'REFUND' in order.name:
                    # raise UserError('Order is already posted to fbr')
                    pass
                elif order.post_data_fbr and order.invoice_number and order.fbr_respone and 'REFUND' in order.name and order.x_studio_refunded_order_posted:
                    # raise UserError('Refund Order is already posted to fbr')
                    pass
                else:
                    orders.append(order.id)

            # raise UserError(str(len(orders)))
            if len(orders) > 0:
                self.post_data_to_fbr(orders)
    
    @api.model
    def _order_fields(self, ui_order):
        if self.company_id.id != 2:

            res = super(POSOrder, self)._order_fields(ui_order)
            res['invoice_number'] = ui_order.get('invoice_number', False)
            res['post_data_fbr'] = ui_order.get('post_data_fbr', False)
            res['fbr_respone'] = ui_order.get('fbr_respone', False)
            return res


        