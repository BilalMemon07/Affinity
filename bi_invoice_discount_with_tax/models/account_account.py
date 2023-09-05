# -*- coding: utf-8 -*-

import odoo.addons.decimal_precision as dp
from odoo import api, fields, models, _
from odoo.tools import float_is_zero, float_compare
from odoo.exceptions import UserError, ValidationError

class account_account(models.Model):
	_inherit = 'account.account'
	
	discount_account = fields.Boolean('Discount Account')
	
	
class account_payment(models.Model):
	_inherit = "account.payment"

	def _prepare_payment_moves(self): 

		res = super(account_payment,self)._prepare_payment_moves()
		for rec in res:
			rec.update({'flag':True})        
		return res
	

