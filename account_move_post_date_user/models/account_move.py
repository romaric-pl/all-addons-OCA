# Copyright 2024 ForgeFlow S.L.
# License LGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo import fields, models


class AccountMove(models.Model):
    _inherit = "account.move"

    last_post_date = fields.Datetime(
        string="Last Posted on", readonly=True, tracking=True
    )
    last_post_uid = fields.Many2one(
        "res.users", string="Last Posted by", readonly=True, tracking=True
    )

    def post(self):
        res = super().post()
        self.write(
            {
                "last_post_date": fields.Datetime.now(),
                "last_post_uid": self.env.user.id,
            }
        )
        return res
