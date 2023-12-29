# Copyright 2023 Camptocamp SA
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl)
{
    "name": "Sale Purchase Stock Line Note",
    "summary": "Propagate sale line note to stock move and purchase",
    "version": "14.0.1.0.0",
    "development_status": "Beta",
    "category": "Hidden",
    "website": "https://github.com/OCA/stock-logistics-workflow",
    "author": "Camptocamp, Odoo Community Association (OCA)",
    "maintainers": ["grindtildeath"],
    "license": "AGPL-3",
    "installable": True,
    "depends": [
        "sale_order_line_note",
        "sale_purchase_stock",
    ],
    "data": [
        "views/purchase_order.xml",
        "views/stock_picking.xml",
    ],
}
