# -*- coding: utf-8 -*-

from odoo import api, fields, models, _

class ResCompany(models.Model):
    _inherit = 'res.company'

    tax_discount_policy = fields.Selection([('tax', 'Tax Amount'), ('untax', 'Untax Amount')],default='untax', )
    sale_account_id = fields.Many2one('account.account',domain=[('account_type', '=', 'expense'), ('discount_account','=',True),])
    purchase_account_id = fields.Many2one('account.account',domain=[('account_type','=','income'), ('discount_account','=',True)])


class ResConfigSettings(models.TransientModel):
    _inherit = 'res.config.settings'

    tax_discount_policy = fields.Selection(readonly=False,related='company_id.tax_discount_policy',string='Discount Applies On',default_model='sale.order'
        )
    sale_account_id = fields.Many2one('account.account',string='Sale Discount Account',check_company=True,domain=[('account_type','=','expense'), ('discount_account','=',True)],readonly=False,related='company_id.sale_account_id')
    purchase_account_id = fields.Many2one('account.account',string='Purchase Discount Account',check_company=True,domain=[('account_type','=','income'), ('discount_account','=',True)],readonly=False,related='company_id.purchase_account_id')