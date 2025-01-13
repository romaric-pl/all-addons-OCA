# Copyright 2024 Camptocamp SA
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl)

import logging

from odoo import SUPERUSER_ID, api

_logger = logging.getLogger(__name__)


def populate_new_field(env):
    records_to_update = (
        env["stock.reception.screen"].search([("current_step", "!=", "done")]).exists()
    )
    _logger.info(
        "Set smaller_package_has_missing_dimensions on ongoing reception screens"
    )
    records_to_update._compute_smaller_package_has_missing_dimensions()


def migrate(cr, version):
    if not version:
        return
    env = api.Environment(cr, SUPERUSER_ID, {})
    populate_new_field(env)
