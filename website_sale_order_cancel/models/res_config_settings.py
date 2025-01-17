# Copyright 2025 Patryk Pyczko (APSL-Nagarro)<ppyczko@apsl.net>
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo import fields, models


class ResConfigSettings(models.TransientModel):
    _inherit = "res.config.settings"

    cancel_restrict_days = fields.Selection(
        selection=[
            ("0", "0 Days (No Restriction)"),
            ("1", "1 Day"),
            ("2", "2 Days"),
            ("3", "3 Days"),
            ("4", "4 Days"),
            ("5", "5 Days"),
            ("6", "6 Days"),
            ("7", "7 Days"),
        ],
        string="Cancel Restriction Days",
        default="1",
        required=True,
        config_parameter="sale.cancel_restrict_days",
        help="Days before delivery date beyond which cancellations are not permitted.",
    )
