# Copyright 2021 Manuel Calero Solís (https://xtendoo.es)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).
{
    'name': 'Sale Order Weight',
    'version': '12.0.1.1.0',
    'category': 'Accounting & Finance',
    'author': 'Xtendoo, Odoo Community Association (OCA)',
    'maintainers': ['legalsylvain'],
    "website": "https://github.com/OCA/sale-workflow",
    'license': 'AGPL-3',
    'summary': 'Sale Order Weight',
    'installable': True,
    'depends': [
        'sale',
        'sale_stock',
    ],
    'data': [
        'views/sale_order_view.xml',
    ],
    'pre_init_hook': 'pre_init_hook',
}
