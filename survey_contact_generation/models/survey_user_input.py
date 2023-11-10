# Copyright 2022 Tecnativa - David Vidal
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).
from odoo import models


class SurveyUserInput(models.Model):
    _inherit = "survey.user_input"

    def _prepare_partner(self):
        """Extract partner values from the answers"""
        self.ensure_one()
        elegible_inputs = self.user_input_line_ids.filtered(
            lambda x: x.question_id.res_partner_field and not x.skipped
        )
        basic_inputs = elegible_inputs.filtered(
            lambda x: x.answer_type not in {"suggestion"}
            and x.question_id.res_partner_field.name != "comment"
        )
        vals = {
            line.question_id.res_partner_field.name: line[f"value_{line.answer_type}"]
            for line in basic_inputs
        }
        for line in elegible_inputs - basic_inputs:
            field_name = line.question_id.res_partner_field.name
            if line.question_id.res_partner_field.ttype == "many2one":
                vals[
                    field_name
                ] = line.value_suggested.res_partner_field_resource_ref.id
            elif line.question_id.res_partner_field.ttype == "many2many":
                vals.setdefault(field_name, [])
                vals[field_name] += [
                    (4, line.value_suggested.res_partner_field_resource_ref.id)
                ]
            # We'll use the comment field to add any other infos
            elif field_name == "comment":
                vals.setdefault("comment", "")
                value = (
                    line.value_suggested.value
                    if line.answer_type == "suggestion"
                    else line[f"value_{line.answer_type}"]
                )
                vals["comment"] += f"\n{line.question_id.title}: {value}"
            else:
                if line.question_id.question_type == "multiple_choice":
                    if not vals.get(field_name):
                        vals[field_name] = line.value_suggested.value
                    else:
                        vals[field_name] += line.value_suggested.value
                else:
                    vals[field_name] = line.value_suggested.value
        return vals

    def _create_contact_post_process(self, partner):
        """After creating the lead send an internal message with the input link"""
        partner.message_post_with_view(
            "mail.message_origin_link",
            values={"self": partner, "origin": self.survey_id},
            subtype_id=self.env.ref("mail.mt_note").id,
        )

    def _mark_done(self):
        """Generate the contact when the survey is submitted"""
        for user_input in self.filtered(
            lambda r: r.survey_id.generate_contact and not self.partner_id
        ):
            vals = user_input._prepare_partner()
            partner = False
            email = vals.get("email")
            if email:
                partner = self.env["res.partner"].search(
                    [("email", "=", email)], limit=1
                )
            if not partner:
                partner = self.env["res.partner"].create(vals)
                self._create_contact_post_process(partner)
            self.update({"partner_id": partner.id, "email": partner.email})
        return super()._mark_done()
