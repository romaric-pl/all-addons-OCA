# Copyright 2019 Ecosoft Co., Ltd (http://ecosoft.co.th/)
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html)

{
    'name': 'Purchase Invoice Plan',
    'summary': 'Add to purchases order, ability to manage future invoice plan',
    'version': '12.0.1.0.2',
    'author': 'Ecosoft,Odoo Community Association (OCA)',
    'license': 'AGPL-3',
    'website': 'https://github.com/OCA/purchase-workflow',
    'category': 'Purchase',
    'depends': ['account',
                'purchase_open_qty',
                'purchase_stock',
                ],
    'data': ['security/ir.model.access.csv',
             'wizard/purchase_create_invoice_plan_view.xml',
             'wizard/purchase_make_planned_invoice_view.xml',
             'views/purchase_view.xml',
             ],
    'installable': True,
    'development_status': 'Alpha',
}