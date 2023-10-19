# -*- coding: utf-8 -*-

from odoo import fields, models

class PosConfig(models.Model):
    _inherit = 'pos.config'

    allow_orderline_user = fields.Boolean(string='Allow Orderline Salesperson', help='Allow custom salesperson on Orderlines')
