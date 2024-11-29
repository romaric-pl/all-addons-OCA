# © 2023 ooops404
# Copyright 2023 Simone Rubino - Aion Tech
# License AGPL-3 - See https://www.gnu.org/licenses/agpl-3.0.html
import json

from odoo import api, fields, models


class ResPartner(models.Model):
    _inherit = "res.partner"

    apply_commission_restrictions = fields.Boolean("Apply Restrictions")
    commission_item_agent_ids = fields.One2many(
        "commission.item.agent", "partner_id", string="Commission Items Groups"
    )
    allowed_commission_group_ids = fields.Many2many(
        "commission.items.group", help="Related only to agents"
    )
    allowed_commission_group_ids_domain = fields.Char(
        compute="_compute_allowed_commission_group_ids_domain",
        readonly=True,
        store=False,
    )
    commission_type = fields.Selection(related="commission_id.commission_type")

    @api.depends("commission_id")
    def _compute_allowed_commission_group_ids_domain(self):
        for rec in self:
            if rec.agent:
                allowed_group_ids = rec.commission_id.filtered(
                    lambda x: x.commission_type == "product_restricted"
                ).item_ids.mapped("group_id")
                rec.allowed_commission_group_ids_domain = json.dumps(
                    [("id", "in", allowed_group_ids.ids)]
                )
            else:
                rec.allowed_commission_group_ids_domain = False

    @api.onchange("agent_ids")
    def _onchange_agent_ids(self):
        for rec in self:
            # ._origin avoids an issue with NewId
            # res.partner(<NewId origin=1>,) != res.partner(1,)
            # but we also need to preserve virtual records (which ._origin discards)
            current_agents = tuple(x._origin or x for x in rec.agent_ids)
            existing_commission_agents = rec.commission_item_agent_ids.mapped(
                "agent_id"
            )
            to_create = [
                {
                    "agent_id": x.id,
                    "group_ids": [(6, 0, x.allowed_commission_group_ids.ids)],
                }
                for x in current_agents
                if (x not in existing_commission_agents)
                and (x.commission_id.commission_type == "product_restricted")
            ]
            to_delete = rec.commission_item_agent_ids.filtered(
                lambda x: x.agent_id not in current_agents
            )
            if to_delete:
                rec.update(
                    {"commission_item_agent_ids": [(2, dl.id, 0) for dl in to_delete]}
                )
            if to_create:
                rec.update(
                    {"commission_item_agent_ids": [(0, 0, line) for line in to_create]}
                )

    @api.onchange("commission_id")
    def _onchange_commission_id(self):
        self.update(
            {
                "allowed_commission_group_ids": [(5, 0, 0)],
            }
        )

    def write(self, vals):
        res = super().write(vals)
        for partner in self:
            if (
                partner.commission_id.commission_type != "product_restricted"
                and partner.allowed_commission_group_ids
            ):
                partner.allowed_commission_group_ids = False
            if "agent" in vals.keys() and not vals["agent"]:
                # not agent anymore - remove related cia's
                cia_records = self.env["commission.item.agent"].search(
                    [("agent_id", "=", partner.id)]
                )
                cia_records.unlink()
        return res
