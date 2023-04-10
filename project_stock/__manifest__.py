# Copyright 2022 Tecnativa - Víctor Martínez
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).
{
    "name": "Project Stock",
    "version": "12.0.1.0.0",
    "category": "Project Management",
    "website": "https://github.com/OCA/project",
    "author": "Tecnativa, Odoo Community Association (OCA)",
    "license": "AGPL-3",
    "depends": ["hr_timesheet", "stock"],
    "installable": True,
    "data": [
        "views/project_project_view.xml",
        "views/project_task_type_view.xml",
        "views/stock_move_view.xml",
        "views/project_task_view.xml",
    ],
    "maintainers": ["victoralmau"],
}
