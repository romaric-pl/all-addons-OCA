# Copyright 2011-2017 Akretion (http://www.akretion.com)
# Copyright 2009-2019 Noviat (http://www.noviat.com)
# @author Alexis de Lattre <alexis.delattre@akretion.com>
# @author Luc de Meyer <info@noviat.com>

from odoo import api, fields, models


class IntrastatTransportMode(models.Model):
    _name = "intrastat.transport_mode"
    _description = "Intrastat Transport Mode"
    _order = "code"
    _sql_constraints = [
        ("intrastat_transport_code_unique", "UNIQUE(code)", "Code must be unique.")
    ]

    code = fields.Char(required=True)
    name = fields.Char(required=True, translate=True)
    description = fields.Char(translate=True)

    @api.depends("name", "code")
    def _compute_display_name(self):
        for mode in self:
            mode.display_name = f"{mode.code}. {mode.name}"
