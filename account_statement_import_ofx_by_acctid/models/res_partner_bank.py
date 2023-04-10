# Copyright 2022 - TODAY, Marcel Savegnago <marcel.savegnago@escodoo.com.br>
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo import api, fields, models

from odoo.addons.base.models.res_bank import sanitize_account_number


class ResPartnerBank(models.Model):

    _inherit = "res.partner.bank"

    acctid = fields.Char("ACCTID")
    sanitized_acctid = fields.Char(
        compute="_compute_sanitized_acctid",
        string="Sanitized ACCTID",
        readonly=True,
        store=True,
    )

    @api.depends("acctid")
    def _compute_sanitized_acctid(self):
        for bank in self:
            bank.sanitized_acctid = sanitize_account_number(bank.acctid)
