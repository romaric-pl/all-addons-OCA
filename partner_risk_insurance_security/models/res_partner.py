from odoo import api, fields, models


class ResPartner(models.Model):
    _inherit = "res.partner"

    is_full_access_user = fields.Boolean(
        string="Is Full Access User",
        compute="_compute_is_full_access_user",
        store=False,
    )

    @api.depends_context("uid")
    def _compute_is_full_access_user(self):
        self.is_full_access_user = self.env.user.has_group(
            "partner_risk_insurance_security.group_full_access_credit_policy_state"
        )
