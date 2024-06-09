# Copyright 2020 Camptocamp SA
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl)
{
    "name": "Stock Move Source Relocation",
    "summary": "Change source location of unavailable moves",
    "version": "14.0.1.3.1",
    "development_status": "Beta",
    "category": "Warehouse Management",
    "website": "https://github.com/OCA/wms",
    "author": "Camptocamp, BCIM, Odoo Community Association (OCA)",
    "maintainers": ["jbaudoux"],
    "license": "AGPL-3",
    "application": False,
    "installable": True,
    "depends": ["stock", "stock_helper"],
    "data": ["views/stock_source_relocate_views.xml", "security/ir.model.access.csv"],
}
