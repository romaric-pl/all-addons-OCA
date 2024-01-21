# Copyright 2022 Camptocamp SA
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).
from odoo import fields, models


class ProjectStatus(models.Model):
    _inherit = "project.status"

    forecast_line_type = fields.Selection(
        [("forecast", "Forecast"), ("confirmed", "Confirmed")],
        help="type of forecast lines created by the tasks of projects in that status",
    )
