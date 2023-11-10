# Copyright 2022 Tecnativa - David Vidal
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).
from odoo import api, fields, models


class SurveyQuestion(models.Model):
    _inherit = "survey.question"

    allowed_field_ids = fields.Many2many(
        comodel_name="ir.model.fields", compute="_compute_allowed_field_ids",
    )
    res_partner_field = fields.Many2one(
        string="Contact field",
        comodel_name="ir.model.fields",
        domain="[('id', 'in', allowed_field_ids)]",
    )

    @api.depends("question_type")
    def _compute_allowed_field_ids(self):
        type_mapping = {
            "textbox": ["char", "text"],
            "free_text": ["text"],
            "numerical_box": ["integer", "float", "text", "char"],
            "date": ["date", "text", "char"],
            "datetime": ["datetime", "text", "char"],
            "simple_choice": ["many2one", "text", "char"],
            "multiple_choice": ["many2many", "text", "char"],
        }
        for record in self:
            record.allowed_field_ids = (
                self.env["ir.model.fields"]
                .search(
                    [
                        ("model", "=", "res.partner"),
                        ("ttype", "in", type_mapping.get(record.question_type, [])),
                    ]
                )
                .ids
            )


class SurveyLabel(models.Model):
    _inherit = "survey.label"

    @api.model
    def default_get(self, fields):
        result = super().default_get(fields)
        if (
            not result.get("res_partner_field")
            or "res_partner_field_resource_ref" not in fields
        ):
            return result
        partner_field = self.env["ir.model.fields"].browse(result["res_partner_field"])
        # Otherwise we'll just use the value (char, text)
        if partner_field.ttype not in {"many2one", "many2many"}:
            return result
        res = self.env[partner_field.relation].search([], limit=1)
        if res:
            result["res_partner_field_resource_ref"] = "%s,%s" % (
                partner_field.relation,
                res.id,
            )
        return result

    @api.model
    def _selection_res_partner_field_resource_ref(self):
        return [(model.model, model.name) for model in self.env["ir.model"].search([])]

    res_partner_field = fields.Many2one(related="question_id.res_partner_field")
    res_partner_field_resource_ref = fields.Reference(
        string="Contact field value",
        selection="_selection_res_partner_field_resource_ref",
    )

    @api.onchange("res_partner_field_resource_ref")
    def _onchange_res_partner_field_resource_ref(self):
        """Set the default value as the product name, although we can change it"""
        if self.res_partner_field_resource_ref:
            self.value = self.res_partner_field_resource_ref.display_name or ""
