# Copyright 2020 Camptocamp
# Copyright 2020-2021 Jacques-Etienne Baudoux (BCIM) <je@bcim.be>
# Copyright 2023 Michael Tietz (MT Software) <mtietz@mt-software.de>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

{
    "name": "Delivery Procurement Group Carrier",
    "Summary": "Record the carrier on the procurement group",
    "version": "14.0.1.1.2",
    "development_status": "Production/Stable",
    "author": "Camptocamp, BCIM, MT Software, Odoo Community Association (OCA)",
    "website": "https://github.com/OCA/stock-logistics-workflow",
    "category": "Warehouse Management",
    "depends": ["sale_stock", "delivery"],
    "data": [
        "views/procurement_group.xml",
    ],
    "installable": True,
    "license": "AGPL-3",
}
