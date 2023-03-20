from datetime import datetime, timedelta
from functools import partial
from itertools import groupby
import requests
import sys
import random
import json
from odoo import api, fields, models, SUPERUSER_ID, _
from odoo.exceptions import AccessError, UserError, ValidationError
from odoo.tools.misc import formatLang, get_lang
from odoo.osv import expression
from odoo.tools import float_is_zero, float_compare
from werkzeug.urls import url_encode
import qrcode
import base64
import io
import pickle
import base64
from base64 import b64encode
from reportlab.lib import units
from reportlab.graphics import renderPM
from reportlab.graphics.barcode import createBarcodeDrawing
from reportlab.graphics.shapes import Drawing
from hashlib import sha256
from hmac import HMAC
from datetime import datetime
import urllib.parse as urlparse
from urllib.parse import urlencode


class ImeiGeneration(models.Model):
    _name = "imei.generation"
    _description = "IMEI Generation"

    name = fields.Char(string='Name', copy=False, readonly=True,
                       index=True, default=lambda self: _('New'))
    mobile_name = fields.Many2one(
        'product.product', string='Mobile Name', required=True)
    sim_type = fields.Selection([('single_sim', 'Single Sim'), (
        '2', '2 Sims'), ('4', '4 Sims')], string='Sim Type', required=True,)
    qty = fields.Integer(required=True, string='Quantity')
    lc_ref = fields.Char(size=4,string="LC Reference", required=True)
    shipment_reference = fields.Char( size=2,
        required=True, string="Shipment Reference")
    imei_lines = fields.One2many('stock.lot', 'imei_id', string='Lines')
    model_no = fields.Char(string="Model No")

    @api.model
    def create(self, vals):
        if vals.get('name', _('New')) == _('New'):
            vals['name'] = self.env['ir.sequence'].next_by_code(
                'name_sq') or _('New')
        res = super(ImeiGeneration, self).create(vals)
        return res


    @api.onchange('mobile_name')
    def set_modelno(self):
        self['model_no'] = self.mobile_name.default_code
    @api.onchange('qty')
    def add_line_items(self):
        for record in self:
            num_items = record.qty
            ids = []
            line_list = []
            if str(self.mobile_name) != 'product.product()':
                if len(str(self.lc_ref)) < 4 or len(str(self.lc_ref)) > 4:
                    raise UserError("LC Reference Must Be 4 Characters long")
                if len(str(self.shipment_reference)) < 2 or len(str(self.shipment_reference)) > 2 :
                    raise UserError("Shipment Reference Must Be 2 Characters long")
            pre_rec = self.env['imei.generation'].search([('model_no', '=', self.model_no), (
                'shipment_reference', '=', self.shipment_reference), ('lc_ref', '=', self.lc_ref)])
            if pre_rec:
                for rec in pre_rec:
                    for line in rec.imei_lines:
                        line_list.append(line)
                lone = line_list[-1]
                for li in lone:
                    number = str(li.serial_no).split(
                        str(self.shipment_reference))[1]
                    c = int(number) + 1

                for i in range(num_items):
                    vals = self.env['ir.sequence'].next_by_code(
                        'serial_sq') or _('New')
                    idd = self.env['stock.lot'].create({
                        'product_id': record.mobile_name.id,
                        'company_id': 1,
                        'simtype': record.sim_type,
                        'model_no': record.mobile_name.default_code,
                        'lc_ref': record.lc_ref,
                        'shipment_ref': record.shipment_reference,
  
                        'serial_no': str(record.mobile_name.default_code) + str(record.lc_ref) + str(record.shipment_reference) + str(c).zfill(6),
                    })
                    c += 1
                    ids.append(idd.id)
                record.write({
                    'imei_lines': [(6, 0, ids)]
                })
            else:

                serial = range(00000, 99999)
                s = list(serial)
                for i in range(num_items):
                    vals = self.env['ir.sequence'].next_by_code(
                        'serial_sq') or _('New')
                    id = self.env['stock.lot'].create({
                        'product_id': record.mobile_name.id,
                        'company_id': 1,
                        'simtype': record.sim_type,
                        'model_no': record.mobile_name.default_code,
                        'lc_ref': record.lc_ref,
                        'shipment_ref': record.shipment_reference,
                        'serial_no': str(record.mobile_name.default_code) + str(record.lc_ref) + str(record.shipment_reference) + str(s[i]).zfill(5),
                    })
                    ids.append(id.id)
                record.write({
                    'imei_lines': [(6, 0, ids)]
                })


class LotSerialLine(models.Model):
    _inherit = "stock.lot"

    imei_id = fields.Many2one('imei.generation')
    simtype = fields.Char(string='Sim Type')
    model_no = fields.Char(string="Model NO")
    product_id = fields.Many2one('product.product')
    shipment_ref = fields.Char('Shipment Reference')
    lc_ref = fields.Char('LC Reference')
    serial_no = fields.Char(string='Serial No')
    serial_no_barcode = fields.Image(string='Serial No Barcode')
    imei_1 = fields.Char(string='IMEI 1')
    imei_1_barcode = fields.Image(string='IMEI 1 Barcode')
    imei_2 = fields.Char(string='IMEI 2')
    imei_2_barcode = fields.Image(string='IMEI 2 Barcode')
    imei_3 = fields.Char(string='IMEI 3')
    imei_3_barcode = fields.Image(string='IMEI 3 Barcode')
    imei_4 = fields.Char(string='IMEI 4')
    imei_4_barcode = fields.Image(string='IMEI 4 Barcode')

    




  
    @api.model
    def create(self, vals):

        imei_code = ''
        for i in range(0,6):
            imei_code += str(random.randint(0, 9))
            imei_1 = '35448464' + str(imei_code)
            checksum = str(self.checksum(imei_1))
        vals['imei_1'] = str(imei_1) + checksum
        if self.simtype != "single" or self.simtype != False:
            imei_code = ''
            checksum = ''
            for j in range(0,6):
                imei_code += str(random.randint(0, 9))
                imei_2 = '35448464'+imei_code
                checksum = str(self.checksum(imei_2))
            vals['imei_2'] = imei_2 + checksum
        if self.simtype != '2' or self.simtype != 'single' or self.simtype != False:
            imei_code = ''
            checksum = ''
            for k in range(0,6):
                imei_code += str(random.randint(0, 9))
                imei_3 = '35448464'+imei_code
                checksum = str(self.checksum(imei_3))
            vals['imei_3'] = imei_3 + checksum
        if self.simtype != '2' or self.simtype != 'single' or self.simtype != False:
            imei_code = ''
            checksum = ''
            for l in range(0,6):
                imei_code += str(random.randint(0, 9))
                imei_4 = '35448464'+imei_code
                checksum = str(self.checksum(imei_4))
            vals['imei_4'] = imei_4 + checksum


# barcodes
    # Barcode for Serial
        img = qrcode.make(self.serial_no)
        result = io.BytesIO()
        img.save(result, format='PNG')
        result.seek(0)
        img_bytes = result.read()
        base64_encoded_result_bytes = base64.b64encode(img_bytes)
        serial_no_barcode = createBarcodeDrawing('Code128', value=str(
            vals['serial_no']), barWidth=0.05 * units.inch, fontSize=30, humanReadable=True)
        width = 600
        drawing_width = width
        barcode_scale = drawing_width / serial_no_barcode.width
        drawing_height = serial_no_barcode.height * barcode_scale
        drawing = Drawing(drawing_width, drawing_height)
        drawing.scale(barcode_scale, barcode_scale)
        drawing.add(serial_no_barcode, name='barcode')
        serial_code = b64encode(renderPM.drawToString(drawing, fmt='PNG'))
        vals['serial_no_barcode'] = serial_code
    # #   For IMEI  1
        img = qrcode.make(self.imei_1)
        result = io.BytesIO()
        img.save(result, format='PNG')
        result.seek(0)
        img_bytes = result.read()
        base64_encoded_result_bytes = base64.b64encode(img_bytes)
        imei_1_bar = createBarcodeDrawing('Code128', value=str(
            vals['imei_1']), barWidth=0.05 * units.inch, fontSize=30, humanReadable=True)
        width = 600
        drawing_width = width
        barcode_scale = drawing_width / imei_1_bar.width
        drawing_height = imei_1_bar.height * barcode_scale
        drawing = Drawing(drawing_width, drawing_height)
        drawing.scale(barcode_scale, barcode_scale)
        drawing.add(imei_1_bar, name='barcode')
        imei_1_code = b64encode(renderPM.drawToString(drawing, fmt='PNG'))
        vals['imei_1_barcode'] = imei_1_code
        if self.simtype != 'single' or self.simtype != False:
            # #  For IMEI 2
            img = qrcode.make(self.imei_2)
            result = io.BytesIO()
            img.save(result, format='PNG')
            result.seek(0)
            img_bytes = result.read()
            base64_encoded_result_bytes = base64.b64encode(img_bytes)
            imei_2_barcode = createBarcodeDrawing('Code128', value=str(
                vals['imei_2']), barWidth=0.05 * units.inch, fontSize=30, humanReadable=True)
            width = 600
            drawing_width = width
            barcode_scale = drawing_width / imei_2_barcode.width
            drawing_height = imei_2_barcode.height * barcode_scale
            drawing = Drawing(drawing_width, drawing_height)
            drawing.scale(barcode_scale, barcode_scale)
            drawing.add(imei_2_barcode, name='barcode')
            imei_2_code = b64encode(renderPM.drawToString(drawing, fmt='PNG'))
            vals['imei_2_barcode'] = imei_2_code
        if self.simtype != '2' or self.simtype != 'single' or self.simtype != False:
            # # For IMEI 3
            img = qrcode.make(self.imei_3)
            result = io.BytesIO()
            img.save(result, format='PNG')
            result.seek(0)
            img_bytes = result.read()
            base64_encoded_result_bytes = base64.b64encode(img_bytes)
            imei_3_barcode = createBarcodeDrawing('Code128', value=str(
                vals['imei_3']), barWidth=0.05 * units.inch, fontSize=30, humanReadable=True)
            width = 600
            drawing_width = width
            barcode_scale = drawing_width / imei_3_barcode.width
            drawing_height = imei_3_barcode.height * barcode_scale
            drawing = Drawing(drawing_width, drawing_height)
            drawing.scale(barcode_scale, barcode_scale)
            drawing.add(imei_3_barcode, name='barcode')
            imei_3_code = b64encode(renderPM.drawToString(drawing, fmt='PNG'))
            vals['imei_3_barcode'] = imei_3_code
        if self.simtype != '2' or self.simtype != 'single' or self.simtype != False:
            # #  For IMEI 4
            img = qrcode.make(self.imei_4)
            result = io.BytesIO()
            img.save(result, format='PNG')
            result.seek(0)
            img_bytes = result.read()
            base64_encoded_result_bytes = base64.b64encode(img_bytes)
            imei_4_barcode = createBarcodeDrawing('Code128', value=str(
                vals['imei_4']), barWidth=0.05 * units.inch, fontSize=30, humanReadable=True)
            width = 600
            drawing_width = width
            barcode_scale = drawing_width / imei_4_barcode.width
            drawing_height = imei_4_barcode.height * barcode_scale
            drawing = Drawing(drawing_width, drawing_height)
            drawing.scale(barcode_scale, barcode_scale)
            drawing.add(imei_4_barcode, name='barcode')
            imei_4_code = b64encode(renderPM.drawToString(drawing, fmt='PNG'))
            vals['imei_4_barcode'] = imei_4_code
        res = super(LotSerialLine, self).create(vals)
        return res
    # def checksum(self,imei):
    #     digits = [int(d) for d in imei]
    #     odd_sum = sum(digits[-1::-2])
    #     even_sum = sum([sum(divmod(2*d, 10)) for d in digits[-2::-2]])
    #     return (10 - (odd_sum + even_sum) % 10) % 10
    
    def checksum(self,number):
    # """
    # Takes in a number and returns the checksum digit for the number
    # """
        # Convert the number to a string
        num_str = str(number)
        
        # Reverse the string
        num_str_reversed = num_str[::-1]
        
        # Initialize variables for the sum and the current digit's position
        current_pos = 1
        total_sum = 0
        
        # Iterate over the reversed string, calculating the sum of the digits
        for digit in num_str_reversed:
            # Convert the digit to an integer
            digit_int = int(digit)
            
            # Multiply the digit by 2 if its position is odd
            if current_pos % 2 != 0:
                digit_int *= 2
                
                # If the result is greater than 9, add the digits of the result
                if digit_int > 9:
                    digit_int = digit_int % 10 + digit_int // 10
                    
            # Add the digit to the sum and move to the next position
            total_sum += digit_int
            current_pos += 1
        
        # Calculate the checksum digit by subtracting the sum from the nearest multiple of 10
        if total_sum % 10 == 0:
            checksum = 0
        else:
            checksum = 10 - (total_sum % 10)
            
        return checksum