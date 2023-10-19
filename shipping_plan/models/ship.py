# -*- coding: utf-8 -*-

from odoo import models, fields, api
from odoo.exceptions import UserError
from odoo.tools import config, human_size, ImageProcess, str2bool, consteq
import base64


class Shipment(models.Model):
    _name = 'shipment.model'
    _description = "Shipment Status"

    name = fields.Char(string="name", store=True)
    line_ids = fields.One2many("shipment.line.model", "shipment_id", string="Line Items", store=True)

class ShipmentLine(models.Model):
    _name = 'shipment.line.model'
    _description = "Shipment Status"

    shipment_id = fields.Many2one("shipment.model",  string="Shipment", store=True)
    Shipment_no = fields.Char(string="Shipment No" , store=True)
    description_of_goods = fields.Char(string="Description of Goods" , store=True)
    current_status= fields.Char(string="Current Status" , store=True)
    qty = fields.Float(string="Qty" , store=True)

    shipment_pickedup = fields.Boolean(string = "Shipment Pickedup")
    tracking_no = fields.Boolean(string = "Tracking No.")
    arrival_at_airport = fields.Boolean(string = "Arrival At Airport")
    shipping_document_submittion_in_bank = fields.Boolean(string = "Shipping Document Submittion in Bank") 
    shipping_documents_received_at_local_bank = fields.Boolean(string = "Shipping Documents Received at local Bank")
    shipping_documents_received_at_shibli = fields.Boolean(string = "Shipping Documents Received at Shibli") 
    do_collection = fields.Boolean(string = "DO Collectio")
    gd_filling_PSID = fields.Boolean(string = "GD Filling + PSID") 
    shipment_clearance = fields.Boolean(string = "Shipment Clearance")
    progress_bar = fields.Integer(string="Progress",  compute="compute_progress")



    @api.depends("shipment_pickedup","tracking_no","arrival_at_airport","shipping_document_submittion_in_bank", "shipping_documents_received_at_local_bank","shipping_documents_received_at_shibli","do_collection","gd_filling_PSID","shipment_clearance")
    def compute_progress(self):
        for rec in self:
            total = 0
            if rec["shipment_pickedup"]:
                total += 10
            if rec["tracking_no"]:
                total += 10
            if rec["arrival_at_airport"]:
                total += 10
            if rec["shipping_document_submittion_in_bank"]:
                total += 10
            if rec["shipping_documents_received_at_local_bank"]:
                total += 10
            if rec["shipping_documents_received_at_shibli"]:
                total += 10
            if rec["do_collection"]:
                total += 10
            if rec["gd_filling_PSID"]:
                total += 15
            if rec["shipment_clearance"]:
                total += 15
            rec['progress_bar'] = total

    
    
           
