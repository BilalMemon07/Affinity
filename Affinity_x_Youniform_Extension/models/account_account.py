import odoo.addons.decimal_precision as dp
from odoo import api, fields, models, _

class account_account(models.Model):
	_inherit = 'account.account'
	
	discount_account = fields.Boolean('Discount Account')
	commission_account = fields.Boolean('Commission Account')
	