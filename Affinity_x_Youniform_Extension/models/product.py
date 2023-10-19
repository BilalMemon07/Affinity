# -*- coding: utf-8 -*-

from odoo import models, fields, api
from odoo.exceptions import UserError
from odoo.tools import config, human_size, ImageProcess, str2bool, consteq
import base64


UOM = [
    ('units', 'Units'),
    ('ctn', 'CTN'),
]
class ProductTemplate(models.Model):
    _inherit = 'product.template'


    commission = fields.Float(string="Commision")
