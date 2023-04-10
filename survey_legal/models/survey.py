# Copyright 2022 Tecnativa - David Vidal
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).
from odoo import fields, models


class SurveySurvey(models.Model):
    _inherit = "survey.survey"

    legal_terms = fields.Boolean(
        string="Require legal terms acceptance",
        help="The users will be prompted to require the acceptance of the legal terms "
        "to be able to submit their answers",
    )
