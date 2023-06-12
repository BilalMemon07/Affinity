from odoo import _, api, fields, models
from odoo.exceptions import ValidationError, UserError



class CityModel(models.Model):
    _name = 'res.city'
    _description = 'res.city'

    name = fields.Char(string='City Name')
    region_id = fields.Many2one('res.region' ,string='Region')

class ProvinceModel(models.Model):
    _name = 'res.province'
    _description = 'res.city'

    name = fields.Char(string='Province Name')

class BusinessNatureModel(models.Model):
    _name = 'res.nature'
    _description = 'res.nature'

    name = fields.Char(string='Business Nature')

class Region(models.Model):
    _name = 'res.region'
    _description = 'res.region'

    name = fields.Char(string='Region Name')
    # cities_id = fields.One2many('res.city', 'region_id', string="Cities" )