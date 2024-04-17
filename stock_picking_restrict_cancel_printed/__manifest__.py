# Copyright 2024 Camptocamp (<https://www.camptocamp.com>).
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

{
    "name": "Stock Picking - restrict cancelation if printed",
    "version": "16.0.1.0.0",
    "development_status": "Beta",
    "category": "Inventory",
    "summary": "Prevent canceling a stock transfer if printed.",
    "author": "Camptocamp, BCIM, Odoo Community Association (OCA)",
    "website": "https://github.com/OCA/stock-logistics-workflow",
    "license": "AGPL-3",
    "depends": ["stock"],
    "data": [
        "views/stock_picking_views.xml",
        "views/stock_picking_type_views.xml",
    ],
    "installable": True,
    "auto_install": False,
}
