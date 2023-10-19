# -*- coding: utf-8 -*-

from odoo import models, fields, api
from odoo.exceptions import UserError
from odoo.tools import config, human_size, ImageProcess, str2bool, consteq
import base64

# from odoo.addons.base.models.ir_attachment import IrAttachment as IA



DELIVERY_STATUS = [
    ('shipment_pickedup','Shipment Pickedup'),
    ('tracking_no','Tracking No.'),
    ('arrival_at_airport', 'Arrival At Airport'),
    ('shipping_document_submittion_in_bank', 'Shipping Document Submittion in Bank'),
    ('shipping_documents_received_at_local_bank', 'Shipping Documents Received at local Bank'),
    ('shipping_documents_received_at_shibli', 'Shipping Documents Received at Shibli'),
    ('do_collection', 'DO Collection'),
    ('gd_filling_PSID', 'GD Filling + PSID'),
    ('shipment_clearance', 'Shipment Clearance'),
]





class StockPicking(models.Model):
    _inherit = 'stock.picking'
    

    shipment_status = fields.Selection(selection=DELIVERY_STATUS,string="Shipment Status",store=True, default='shipment_pickedup')
    qty = fields.Float(string="Quantity", store=True)
    progress_bar = fields.Integer(string="Progress Bar", store=True, compute="compute_progress")


    shipment_pickedup = fields.Boolean(string = "Shipment Pickedup")
    tracking_no = fields.Boolean(string = "Tracking No.")
    arrival_at_airport = fields.Boolean(string = "Arrival At Airport")
    shipping_document_submittion_in_bank = fields.Boolean(string = "Shipping Document Submittion in Bank") 
    shipping_documents_received_at_local_bank = fields.Boolean(string = "Shipping Documents Received at local Bank")
    shipping_documents_received_at_shibli = fields.Boolean(string = "Shipping Documents Received at Shibli") 
    do_collection = fields.Boolean(string = "DO Collectio")
    gd_filling_PSID = fields.Boolean(string = "GD Filling + PSID") 
    shipment_clearance = fields.Boolean(string = "Shipment Clearance")
   


    @api.model
    def create(self,vals):
        # if vals.get('name', _('New')) == _('New'):
        # vals['state'] = 'Idle'
        vals['shipment_pickedup'] = True
        vals['shipment_status'] = 'shipment_pickedup'

        
        res = super(StockPicking,self).create(vals)
        return res
    


    
    @api.depends("shipment_status")
    def compute_progress(self):
        for rec in self:

            if rec.shipment_status == "shipment_pickedup":
                rec['progress_bar'] = 10
            elif rec.shipment_status == "tracking_no":
                rec['progress_bar'] = 20
            elif rec.shipment_status == "arrival_at_airport":
                rec['progress_bar'] = 30
            elif rec.shipment_status == "shipping_document_submittion_in_bank":
                rec['progress_bar'] = 40
            elif rec.shipment_status == "shipping_documents_received_at_local_bank":
                rec['progress_bar'] = 50
            elif rec.shipment_status == "shipping_documents_received_at_shibli":
                rec['progress_bar'] = 60
            elif rec.shipment_status == "do_collection":
                rec['progress_bar'] = 70
            elif rec.shipment_status == "gd_filling_PSID":
                rec['progress_bar'] = 85
            elif rec.shipment_status == "shipment_clearance":
                rec['progress_bar'] = 100
            else:
                rec['progress_bar'] = 0
        self.create_plan_record()


    def create_plan_record(self):
        ship = self.env['shipment.model'].search([(
            "name" ,"=","ABC"
        )])
        # raise UserError(ship)
        list_line = []
        if ship:
            if len(ship.line_ids) == 0:
                obj = {
                    "Shipment_no": self.name,
                    'shipment_pickedup':self['shipment_pickedup'],
                    'tracking_no': self['tracking_no'],
                    'arrival_at_airport' :self['arrival_at_airport'],
                    'shipping_document_submittion_in_bank': self['shipping_document_submittion_in_bank'],
                    'shipping_documents_received_at_local_bank' :self['shipping_documents_received_at_local_bank'],
                    'shipping_documents_received_at_shibli' :self['shipping_documents_received_at_shibli'],
                    'do_collection' :self['do_collection'],
                    'gd_filling_PSID':self['gd_filling_PSID'],
                    'shipment_clearance':self['shipment_clearance'],
                }
                list_line.append((0,0,obj))
                ship.write({
                    'line_ids':list_line
                })
                list_line = []
            
            elif len(ship.line_ids) != 0:
                check_list = []
                for line in ship.line_ids:
                    check_list.append(line.Shipment_no)
                # raise UserError(str(check_list))
                lines = self.env['shipment.line.model'].search([('Shipment_no', '=' ,self.name), ('shipment_id', '=' ,ship.id)])
                if self.name in check_list:
                    for line in lines:
                        lines.write({
                            "Shipment_no" :  self.name,
                            'shipment_pickedup' : self['shipment_pickedup'],
                            'tracking_no' : self['tracking_no'],
                            'arrival_at_airport' : self['arrival_at_airport'],
                            'shipping_document_submittion_in_bank' :  self['shipping_document_submittion_in_bank'],
                            'shipping_documents_received_at_local_bank' : self['shipping_documents_received_at_local_bank'],
                            'shipping_documents_received_at_shibli' : self['shipping_documents_received_at_shibli'],
                            'do_collection' : self['do_collection'],
                            'gd_filling_PSID' : self['gd_filling_PSID'],
                            'shipment_clearance' : self['shipment_clearance'],
                        })
                        break
                if self.name not in check_list:
                    obj = {
                        "Shipment_no": self.name,
                        'shipment_pickedup':self['shipment_pickedup'],
                        'tracking_no': self['tracking_no'],
                        'arrival_at_airport' :self['arrival_at_airport'],
                        'shipping_document_submittion_in_bank': self['shipping_document_submittion_in_bank'],
                        'shipping_documents_received_at_local_bank' :self['shipping_documents_received_at_local_bank'],
                        'shipping_documents_received_at_shibli' :self['shipping_documents_received_at_shibli'],
                        'do_collection' :self['do_collection'],
                        'gd_filling_PSID':self['gd_filling_PSID'],
                        'shipment_clearance':self['shipment_clearance'],
                    }
                    list_line.append((0,0,obj))
                    ship.write({
                        'line_ids':list_line
                    })
                    list_line = []
                    
                    # ship['line_ids'] = list_line
                

        
    # def create_shipment_plan_record(self, delivery_status_obj):
    #     for rec in self:
    #         exist  = self.env['shipment.model'].search([("name" ,'=', "Bilal Testing")])
    #         if not exist:
    #             self.env['shipment.model'].create({
    #                 "name":"Bilal Testing"
    #             })
    #         else:
    #             for line in exist.line_ids:
    #                 if line.Shipment_no != rec.name:
    #                     obj = {
                            
    #                         'shipment_pickedup':False,
    #                         'tracking_no':False,
    #                         'arrival_at_airport' :False,
    #                         'shipping_document_submittion_in_bank': False,
    #                         'shipping_documents_received_at_local_bank' :False,
    #                         'shipping_documents_received_at_shibli' :False,
    #                         'do_collection' :False,
    #                         'gd_filling_PSID':False,
    #                         'shipment_clearance':False,
    #                     }






    def shipment_next_step(self):

        for rec in self:
            if rec.shipment_status == "shipment_pickedup":
                rec['shipment_status'] = "tracking_no"
                rec['tracking_no'] = True
            elif rec.shipment_status == "tracking_no":
                rec['shipment_status'] = "arrival_at_airport"                
                rec['arrival_at_airport'] = True
            elif rec.shipment_status == "arrival_at_airport":
                rec['shipment_status'] = "shipping_document_submittion_in_bank"
                rec['shipping_document_submittion_in_bank'] = True
            elif rec.shipment_status == "shipping_document_submittion_in_bank":
                rec['shipment_status'] = "shipping_documents_received_at_local_bank"
                rec['shipping_documents_received_at_local_bank'] = True
            elif rec.shipment_status == "shipping_documents_received_at_local_bank":
                rec['shipment_status'] = "shipping_documents_received_at_shibli"
                rec['shipping_documents_received_at_shibli'] = True
            elif rec.shipment_status == "shipping_documents_received_at_shibli":
                rec['shipment_status'] = "do_collection"
                rec['do_collection'] = True
            elif rec.shipment_status == "do_collection":
                rec['shipment_status'] = "gd_filling_PSID"
                rec['gd_filling_PSID'] = True
            elif rec.shipment_status == "gd_filling_PSID":
                rec['shipment_status'] = "shipment_clearance"
                rec['shipment_clearance'] = True



             




    