# Copyright (C) 2016 Forest and Biomass Romania
# Copyright (C) 2022 NextERP Romania
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from odoo import models


class AccountBankStatementImport(models.TransientModel):
    _inherit = "account.statement.import"

    def _is_brd(self):
        if self._context.get("journal_id"):
            journal = self.env["account.journal"].browse(self._context["journal_id"])
            return journal.bank_account_id.bank_bic == "BRDEROBU"
        return self._context.get("mt940_ro_brd")

    def _parse_file(self, data_file):
        if self._is_brd():
            parser = self.env["l10n.ro.account.bank.statement.import.mt940.parser"]
            parser = parser.with_context(type="mt940_ro_brd")
            data = parser.parse(data_file)
            if data:
                return data
        return super()._parse_file(data_file)
