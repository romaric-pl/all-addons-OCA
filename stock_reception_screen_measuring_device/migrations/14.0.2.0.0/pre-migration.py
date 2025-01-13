# Copyright 2021 Camptocamp SA
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl)

import logging

_logger = logging.getLogger(__name__)


def create_and_populate_new_fields(cr):
    cr.execute(
        """
        ALTER TABLE stock_reception_screen
        ADD COLUMN IF NOT EXISTS smaller_package_has_missing_dimensions BOOLEAN;
        """
    )
    # Set value to False for done reception screens.
    # Otherwise, let the ORM do its job in post migration
    _logger.info("Set smaller_package_has_missing_dimensions on done reception screens")
    cr.execute(
        """
        UPDATE stock_reception_screen
        SET smaller_package_has_missing_dimensions = FALSE
        WHERE current_step = 'done';
        """
    )


def migrate(cr, version):
    create_and_populate_new_fields(cr)
