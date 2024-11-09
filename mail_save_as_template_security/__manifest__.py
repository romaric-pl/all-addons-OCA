# Copyright 2024 Alberto Martínez <alberto.martinez@sygel.es>
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).
{
    "name": "Mail Save As Template Security",
    "summary": "Restrict save as new template button from the send email wizard",
    "version": "15.0.1.0.0",
    "category": "Productivity/Discuss",
    "website": "https://github.com/OCA/social",
    "author": "Sygel, Odoo Community Association (OCA)",
    "maintainers": ["tisho99"],
    "license": "AGPL-3",
    "application": False,
    "installable": True,
    "depends": [
        "mail",
    ],
    "data": [
        "security/mail_save_as_template_security.xml",
        "wizard/mail_compose_message_view.xml",
    ],
}
