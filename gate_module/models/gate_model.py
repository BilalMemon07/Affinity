# -*- coding: utf-8 -*-
from odoo import api, fields, models,_
from odoo.exceptions import UserError
from datetime import datetime

class GateINModule(models.Model):
    _name = "gate.in"
    _description = "Gate Module"

    name = fields.Char(string='Gate Reference', required=True, copy=False, readonly=True,
                           index=True, default=lambda self: _('New'))
    vendor_type = fields.Selection([('vendor', 'Vendor'),('sampling', 'Sampling'),('ho', 'HO'), ('other', 'Other')], string='Gate In Vendor Type' ,required=True,)
    gate_type = fields.Selection([('returnable', 'Returnable'), ('nonreturnable', 'Non Returnable')], string='Gate In Type', required=True,)
    partner_id = fields.Many2one('res.partner',string='Partner')
    vendor_name= fields.Char(string='Vendor')
    purchase_id = fields.Many2one('purchase.order',string='Purchase Order')
    return_date = fields.Date(string='Return Date',)
    line_id = fields.One2many('gate.vendor.line', 'gate_module_id', string="Gate Line")
    line_ids = fields.One2many('gate.other.line', 'gate_module_id', string="Gate Line")
    
    location_name = fields.Selection([('unit_one', 'Unit One'),('ho', 'HO')],string="Location Name")
    receiver_name = fields.Char(string="Receiver Name")
    department = fields.Char(string="Department")
    department_id = fields.Many2one('stock.location' , string="Department")
    attention_to = fields.Char(string="Attention To")
    date_time = fields.Datetime(string="Date Time")
    saneder_name = fields.Char(string="Sender Name")
    saneder_number= fields.Char(string="Sender Number")
    vehicle_number= fields.Char(string="Vehicle Number")
    phone  = fields.Binary(string="Photo")

    state = fields.Selection([('draft', "Draft"),('done', "Done"),])

    # @api.multi
    # def action_draft(self):

    #     self.state = 'draft'

    # @api.multi
    # def action_done(self):
    #     self.state = 'done'

    def post_action(self):
        self.state = 'done'
        # raise UserError("Hello Worlds")

    @api.model
    def create(self,vals):
        if vals.get('name', _('New')) == _('New'):
            vals['name'] = self.env['ir.sequence'].next_by_code('Gate_IN') or _('New')
            vals['date_time']= datetime.now()
            vals['state']= 'draft'
        res = super(GateINModule,self).create(vals)
        return res
    
    
    @api.onchange("partner_id")
    def partner_id_domain_pur(self):
        if self.partner_id:
            return {"domain": {'partner_id': [('supplier_rank', '>', '0')]}}

    
    @api.onchange("partner_id","purchase_id")
    def purchase_order_domain_pur(self):
        if self.partner_id : 
            return {"domain": {'purchase_id': [('partner_id', '=', self.partner_id.id)]}}
    
    @api.onchange('purchase_id')
    def _onchange_all_po_line(self):
        order_line=[]
        self['line_id'] = False
        for record in self:
            if record.purchase_id:
                other_model_record = self.env['purchase.order'].search([('id','=', record.purchase_id.id)])
                # raise UserError(other_model_record)
                if other_model_record:
                    for rec in other_model_record:
                        for line in rec.order_line:
                            order_line.append((0,0,{
                                'product_id': line.product_id.id,
                                'product_uom_id': line.product_uom.id
                            }))
                self['line_id'] = order_line

       
class GateInLine(models.Model):
    _name = 'gate.vendor.line'
    _description = "Gate Line"

    gate_module_id = fields.Many2one('gate.in')
    product_id = fields.Many2one('product.product',string='Product')
    product_uom_id = fields.Many2one('uom.uom',string='Unit Of Measurement')
    qty = fields.Float(string='Quantity')
        
class GateInLine_(models.Model):
    _name = 'gate.other.line'
    _description = "Gate Lines"

    gate_module_id = fields.Many2one('gate.in')
    product = fields.Char(string='Product')
    product_uom = fields.Char(string='Unit Of Measurement')
    qty = fields.Float(string='Quantity')

class GateOutModule(models.Model):
    _name = "gate.out"
    _description = "Gate Out Module"

    name = fields.Char(string='Gate Reference', required=True, copy=False, readonly=True,
                           index=True, default=lambda self: _('New'))
    doc_type = fields.Selection([('g_in', 'Gate In'), ('g_out', 'Gate Out')], string='Document Type')
    customer_type = fields.Selection([('customer', 'Customer'), ('market', 'Market'),('sampling', 'Sampling'),('ho', 'HO'), ('other', 'Other')], string='Gate Out Customer Type')
    gate_type = fields.Selection([('returnable', 'Returnable'), ('nonreturnable', 'Non Returnable')], string='Gate Out Type')
    partner_id = fields.Many2one('res.partner',string='Partner')
    customer_name= fields.Char(string='Customer')
    sale_id = fields.Many2one('stock.picking',string='Delivery Order')
    return_date = fields.Date(string='Return Date',)
    line_id = fields.One2many('gate.customer.line', 'gate_module_id', string="Gate Line")
    line_ids = fields.One2many('gate.other.lines', 'gate_module_id', string="Gate Line")

    location_name = fields.Selection([('fabric', 'FABRIC'),('unit_one', 'Unit One'),('ho', 'HO'),('fg', 'FG'),('e-comm', 'E-Comm'),('whole sale', 'Whole Sale'),('other', 'Other')],string="Location Name")
    sender_name = fields.Char(string="Sender Name")
    department = fields.Char(string="Department")
    department_id = fields.Many2one('stock.location' , string="Department")
    attention_to = fields.Char(string="Attention To")
    date_time = fields.Datetime(string="Date Time")
    receiver_name = fields.Char(string="Receiver Name")
    receiver_number= fields.Char(string="Receiver Number")
    vehicle_number= fields.Char(string="Vehicle Number")
    phone  = fields.Binary(string="Photo")
    state = fields.Selection([('draft', "Draft"),('done', "Done"),])

    @api.model
    def create(self,vals):
        if vals.get('name', _('New')) == _('New'):
            vals['name'] = self.env['ir.sequence'].next_by_code('Gate_OUT') or _('New')
            vals['state'] = 'draft'
            vals['date_time']= datetime.now()
        res = super(GateOutModule,self).create(vals)
        return res
    
    def post_action(self):
        self.state = 'done'
    
    @api.onchange("partner_id")
    def partner_id_domain_pur(self):
        if self.partner_id:
            return {"domain": {'partner_id': [('customer_rank', '>', '0')]}}

    
    @api.onchange("partner_id","sale_id")
    def purchase_order_domain_pur(self):
        if self.partner_id:
            return {"domain": {'sale_id': [('partner_id', '=', self.partner_id.id)]}}
    
    
    @api.onchange('sale_id')
    def _onchange_all_so_line(self):
        order_line=[]
        self['line_id'] = False
        for record in self:
            if record.sale_id:
                other_model_record = self.env['stock.picking'].search([('id','=', record.sale_id.id)])
                # raise UserError(other_model_record)
                if other_model_record:
                    for rec in other_model_record:
                        for line in rec.move_ids_without_package:
                            order_line.append((0,0,{
                                'product_id': line.product_id.id,
                                'product_uom_id': line.product_uom.id
                            }))
                self['line_id'] = order_line
    
        
class GateOutLine(models.Model):
    _name = 'gate.customer.line'
    _description = "Gate Line"

    gate_module_id = fields.Many2one('gate.out')
    product_id = fields.Many2one('product.product',string='Product')
    product_uom_id = fields.Many2one('uom.uom',string='Unit Of Measurement')
    # product_uom_id = fields.Char(string='Unit Of Measurement')
    qty = fields.Float(string='Quantity')
        
class GateOutLine_(models.Model):
    _name = 'gate.other.lines'
    _description = "Gate Lines"

    gate_module_id = fields.Many2one('gate.out')
    product = fields.Char(string='Product')
    product_uom = fields.Char(string='Unit Of Measurement')
    qty = fields.Float(string='Quantity')
