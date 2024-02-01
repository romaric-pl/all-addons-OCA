# Copyright 2019 Ecosoft Co., Ltd (http://ecosoft.co.th/)
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html)

{
    "name": "Thai Localization - VAT and Withholding Tax",
    "version": "16.0.1.1.0",
    "author": "Ecosoft, Odoo Community Association (OCA)",
    "license": "AGPL-3",
    "website": "https://github.com/OCA/l10n-thailand",
    "category": "Localization / Accounting",
    "depends": ["account"],
    "data": [
        "data/pit_rate_data.xml",
        "data/withholding_tax_type_income_data.xml",
        "security/account_security.xml",
        "security/ir.model.access.csv",
        "wizard/account_payment_register_views.xml",
        "wizard/account_move_reversal_view.xml",
        "views/res_config_settings_views.xml",
        "views/account_view.xml",
        "views/account_tax_view.xml",
        "views/account_move_view.xml",
        "views/withholding_tax_cert.xml",
        "views/account_withholding_tax.xml",
        "views/withholding_tax_code_income.xml",
        "views/account_withholding_move.xml",
        "views/product_view.xml",
        "views/account_payment_view.xml",
        "views/personal_income_tax_view.xml",
        "views/res_partner_view.xml",
        "views/account_menu.xml",
    ],
    "installable": True,
    "development_status": "Beta",
    "maintainers": ["kittiu"],
}