# Copyright 2020 Tecnativa - Carlos Roca
# License AGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

{
    "name": "Stock Picking Product Assortment",
    "version": "15.0.2.0.0",
    "category": "Warehouse Management",
    "website": "https://github.com/OCA/stock-logistics-workflow",
    "author": "Tecnativa, Odoo Community Association (OCA)",
    "maintainers": ["CarlosRoca13"],
    "license": "AGPL-3",
    "installable": True,
    "depends": ["base_view_inheritance_extension", "product_assortment", "stock"],
    "data": ["views/stock_picking_view.xml"],
}
