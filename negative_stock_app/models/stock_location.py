from odoo import fields, models


class StockLocation(models.Model):
    _inherit = "stock.location"

    allow_negative_stock = fields.Boolean(
        help="Allow negative stock levels for the stockable products "
        "attached to this location.",
    )
