# Copyright 2021 Camptocamp
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).
{
    "name": "Mass Scrap",
    "summary": "Add wizard to mass scrap expired products",
    "version": "14.0.1.0.1",
    "category": "Inventory",
    "website": "https://github.com/OCA/stock-logistics-workflow",
    "author": "Camptocamp, Odoo Community Association (OCA)",
    "license": "AGPL-3",
    "depends": [
        "product_expiry",
        "stock",
    ],
    "data": [
        # Data
        "data/ir_actions_server.xml",
        # Security
        "security/ir.model.access.csv",
        # Wizards
        "wizard/mass_scrap.xml",
    ],
    "installable": True,
}
