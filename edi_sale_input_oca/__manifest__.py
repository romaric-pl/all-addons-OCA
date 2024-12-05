# Copyright 2022 Camptocamp SA
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

{
    "name": "EDI Sales input",
    "summary": """
        Process incoming sale orders with the EDI framework.
    """,
    "version": "14.0.1.1.0",
    "development_status": "Alpha",
    "license": "AGPL-3",
    "author": "Camptocamp,Odoo Community Association (OCA)",
    "maintainers": ["simahawk"],
    "website": "https://github.com/OCA/edi",
    "depends": [
        "edi_sale_oca",
        "edi_record_metadata_oca",
        "sale_order_import",
    ],
    "data": [],
    "demo": [
        "demo/edi_exchange_type.xml",
    ],
}
