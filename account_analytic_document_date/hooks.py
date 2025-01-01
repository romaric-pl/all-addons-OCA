# Copyright 2024 (APSL - Nagarro) Miquel Pascual, Bernat Obrador
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).


def post_init_hook(cr, registry):
    cr.execute(
        """
        UPDATE account_move
        SET analytic_document_date = invoice_date
        WHERE analytic_document_date IS NULL
    """
    )
