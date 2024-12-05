# Copyright 2024 Camptocamp SA
# @author: Simone Orsi <simahaw@gmail.com>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).


from odoo import fields, models


class ResPartner(models.Model):
    _inherit = "res.partner"

    edi_sale_conf_ids = fields.Many2many(
        string="EDI sale configuration",
        comodel_name="edi.configuration",
        relation="res_partner_edi_sale_configuration_rel",
        column1="partner_id",
        column2="conf_id",
        domain=[("model_name", "=", "sale.order")],
    )
