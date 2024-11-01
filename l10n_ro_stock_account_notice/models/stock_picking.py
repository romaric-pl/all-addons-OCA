# Copyright (C) 2014 Forest and Biomass Romania
# Copyright (C) 2020 NextERP Romania
# Copyright (C) 2020 Terrabit
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from odoo import fields, models


class StockPickingType(models.Model):
    _name = "stock.picking.type"
    _inherit = ["stock.picking.type", "l10n.ro.mixin"]

    l10n_ro_notice_default = fields.Boolean(string="Romania - Is a notice")


class StockPicking(models.Model):
    _name = "stock.picking"
    _inherit = ["stock.picking", "l10n.ro.mixin"]

    def _get_notice(self):
        res = False
        company = self.env.company
        company_id = self.env.context.get("default_company_id", False)
        if company_id:
            company = self.env["res.company"].browse(company_id)
        if company.chart_template == "ro":
            picking_type_id = self.env.context.get("default_picking_type_id", False)
            picking_type = self.env["stock.picking.type"].browse(picking_type_id)
            if picking_type:
                res = picking_type.l10n_ro_notice_default
        return res

    # Prin acest camp se indica daca un produs care e stocabil trece prin
    # contul 408 / 418 la achizitie sau vanzare
    # receptie/ livrare in baza de aviz
    l10n_ro_notice = fields.Boolean(
        string="Romania - Is a notice",
        default=_get_notice,
        help="This field sets the reception/delivery as a notice."
        " The resulting account move will include accounts 408/418.",
    )
