# Copyright 2022-2023 Moduon Team S.L. <info@moduon.team>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).
from logging import getLogger

from odoo import _, models
from odoo.exceptions import ValidationError

_logger = getLogger(__name__)


class ResConfigSettings(models.TransientModel):
    _inherit = "res.config.settings"

    def execute_update_check_vies(self):
        """Bulk VAT check on company partners."""
        partners = self.env["res.partner"].search(
            [
                ("is_company", "=", True),
                ("parent_id", "=", False),
                ("vat", "!=", False),
                ("vies_passed", "=", False),
            ]
        )
        failures = 0
        for partner in partners:
            try:
                partner.check_vat()
            except ValidationError:
                _logger.warning("VAT check failed for %r", partner, exc_info=True)
                failures += 1
        return {
            "effect": {
                "fadeout": "slow",
                "message": _(
                    "Vies passed calculated in %(partners)d partners (%(failures)d failures)",
                    partners=len(partners),
                    failures=failures,
                ),
                "img_url": "/web/static/img/smile.svg",
                "type": "rainbow_man",
            }
        }
