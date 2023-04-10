# Copyright 2017 ForgeFlow S.L.
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).
{
    "name": "Purchase Order Approved",
    "summary": "Add a new state 'Approved' in purchase orders.",
    "version": "14.0.1.2.1",
    "category": "Purchases",
    "website": "https://github.com/OCA/purchase-workflow",
    "author": "ForgeFlow, ACSONE SA/NV, Odoo Community Association (OCA)",
    "license": "AGPL-3",
    "application": False,
    "installable": True,
    "depends": ["purchase_stock"],
    "data": [
        "views/res_partner.xml",
        "views/purchase_order_view.xml",
        "views/res_config_view.xml",
    ],
}
