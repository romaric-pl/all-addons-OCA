# Copyright 2022 Camptocamp SA
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

{
    "name": "EDI Sales",
    "summary": """
        Configuration and special behaviors for EDI on sales.
    """,
    "version": "14.0.2.0.0",
    "development_status": "Alpha",
    "license": "AGPL-3",
    "author": "Camptocamp,Odoo Community Association (OCA)",
    "maintainers": ["simahawk"],
    "website": "https://github.com/OCA/edi",
    "depends": [
        "edi_oca",
        "edi_record_metadata_oca",
        "sale",
    ],
    "data": [
        "views/res_partner.xml",
        "views/sale_order.xml",
        "views/edi_exchange_record.xml",
    ],
    "demo": [
        "demo/edi_backend.xml",
        "demo/edi_exchange_type.xml",
    ],
}
