# Copyright (C) 2016-Today: Odoo Community Association (OCA)
# @author: Sylvain LE GAL (https://twitter.com/legalsylvain)
# Copyright 2024 Tecnativa - Carolina Fernandez
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).
{
    "name": "Github Connector - Odoo",
    "summary": "Analyze Odoo modules information from Github repositories",
    "version": "17.0.1.0.0",
    "category": "Connector",
    "license": "AGPL-3",
    "author": "Odoo Community Association (OCA), Sylvain LE GAL, GRAP",
    "website": "https://github.com/OCA/interface-github",
    "depends": ["github_connector"],
    "data": [
        "security/ir.model.access.csv",
        "data/function.xml",
        "views/view_reporting.xml",
        "views/action.xml",
        "views/menu.xml",
        "views/view_odoo_license.xml",
        "views/view_odoo_author.xml",
        "views/view_odoo_lib_bin.xml",
        "views/view_odoo_lib_python.xml",
        "views/view_odoo_module.xml",
        "views/view_odoo_module_version.xml",
        "views/view_github_analysis_rule.xml",
        "views/view_github_organization.xml",
        "views/view_github_repository.xml",
        "views/view_github_repository_branch.xml",
        "data/odoo_licence.xml",
        "data/odoo_category_data.xml",
        "data/odoo_manifest_key_data.xml",
        "data/ir_cron.xml",
        "report/odoo_module_version_rule_info_report_view.xml",
    ],
    "demo": [
        "demo/github_analysis_rule_group_demo.xml",
        "demo/github_analysis_rule_demo.xml",
        "demo/github_organization.xml",
    ],
    "installable": True,
    "external_dependencies": {"python": ["pathspec"]},
}
