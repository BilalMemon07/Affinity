# -*- coding: utf-8 -*-

from odoo import api, fields, models

class PosOrder(models.Model):
	_inherit = "pos.order"

	allow_orderline_user = fields.Boolean(related='session_id.config_id.allow_orderline_user')


class PosOrderLine(models.Model):
	_inherit = "pos.order.line"

	salesperson_id = fields.Many2one('hr.employee', string='Salesperson',
										help='Salesperson who selected in pos')

