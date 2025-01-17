# Copyright 2019 Tecnativa - Vicent Cubells
# Copyright 2019 Tecnativa - Pedro M. Baeza
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).
{
    "name": "Delivery Free Fee Removal",
    "summary": "Hide free fee lines on sales orders",
    "version": "17.0.1.0.0",
    "category": "Delivery",
    "website": "https://github.com/OCA/delivery-carrier",
    "author": "Tecnativa, Camptocamp, Odoo Community Association (OCA)",
    "installable": True,
    "license": "AGPL-3",
    "depends": ["delivery"],
    "data": ["views/sale_order_views.xml", "reports/sale_report_templates.xml"],
}
