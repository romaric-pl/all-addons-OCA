from odoo import fields, models


class ResConfigSettings(models.TransientModel):
    _inherit = "res.config.settings"

    timesheet_product_id = fields.Many2one(
        "product.product",
        related="company_id.timesheet_product_id",
        string="Purchase Timesheet Product",
        readonly=False,
    )
