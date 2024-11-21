# Copyright 2024 Moduon Team S.L.
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl-3.0)

{
    "name": "Account Chart Update Multilang",
    "summary": "Update tax and fiscal position templates with multilang",
    "version": "16.0.1.0.2",
    "development_status": "Alpha",
    "category": "Accounting",
    "website": "https://github.com/OCA/account-financial-tools",
    "author": "Moduon, Odoo Community Association (OCA)",
    "maintainers": ["edlopen", "rafaelbn"],
    "license": "AGPL-3",
    "auto_install": True,
    "installable": True,
    "depends": [
        "account_chart_update",
        "l10n_multilang",
    ],
    "data": [
        "wizards/wizard_chart_update_views.xml",
    ],
}
