# Copyright 2024 Quartile
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

from odoo import fields, models


class ResCompany(models.Model):
    _inherit = "res.company"

    lock_qty_done = fields.Boolean(
        string="Limit Updates to Done Quantity After Validation",
        help="Only users in the 'Can Edit Done Quantity for Done Stock Moves' group"
        " are allowed to edit the 'done' quantity for validated transfer.",
    )
