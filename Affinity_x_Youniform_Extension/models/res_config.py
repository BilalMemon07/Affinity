# -*- coding: utf-8 -*-

from odoo import api, fields, models, _

class ResCompany(models.Model):
    _inherit = 'res.company'

    commission_account_id = fields.Many2one('account.account',string='Commission Account',domain=[('account_type', '=', 'liability_current'), ('commission_account','=',True),])
    discount_account_id = fields.Many2one('account.account',string='Discount Account',domain=[('account_type','=','expense'), ('discount_account','=',True)])
    journal_id = fields.Many2one('account.journal',string='Journal')


class ResConfigSettings(models.TransientModel):
    _inherit = 'res.config.settings'


    commission_account_id = fields.Many2one('account.account',string='Commission Account',check_company=True,domain=[('account_type','=','liability_current'), ('commission_account','=',True)],readonly=False,related='company_id.commission_account_id')
    discount_account_id = fields.Many2one('account.account',string='Discount Account',check_company=True,domain=[('account_type','=','expense'), ('discount_account','=',True)],readonly=False,related='company_id.discount_account_id')
    journal_id = fields.Many2one('account.journal',string='Journal', check_company=True, readonly=False, related='company_id.journal_id',)