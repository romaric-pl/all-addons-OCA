# Copyright 2022 CreuBlanca
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

{
    "name": "Mgmtsystem Evaluation",
    "summary": """
        Evaluate records within your management system""",
    "version": "14.0.1.0.0",
    "license": "AGPL-3",
    "author": "CreuBlanca,Odoo Community Association (OCA)",
    "website": "https://github.com/OCA/management-system",
    "depends": ["mgmtsystem", "mail"],
    "data": [
        "security/security.xml",
        "security/ir.model.access.csv",
        "views/mgmtsystem_evaluation_result.xml",
        "views/mgmtsystem_evaluation_template.xml",
        "views/mgmtsystem_evaluation.xml",
        "templates/asset_backend.xml",
        "views/res_partner.xml",
    ],
    "demo": ["demo/demo.xml"],
}
