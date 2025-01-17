# Copyright 2018 ForgeFlow, S.L.
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo import _, api, fields, models
from odoo.exceptions import ValidationError


class HrDepartment(models.Model):
    _inherit = "hr.department"

    timesheet_sheet_to_approve_count = fields.Integer(
        compute="_compute_timesheet_to_approve", string="Timesheet Sheets to Approve"
    )

    def _compute_timesheet_to_approve(self):
        timesheet_data = self.env["hr_timesheet.sheet"].read_group(
            [("department_id", "in", self.ids), ("state", "=", "confirm")],
            ["department_id"],
            ["department_id"],
        )
        result = {
            data["department_id"][0]: data["department_id_count"]
            for data in timesheet_data
        }
        for department in self:
            department.timesheet_sheet_to_approve_count = result.get(department.id, 0)

    @api.constrains("company_id")
    def _check_company_id(self):
        for rec in self.sudo().filtered("company_id"):
            for field in [
                rec.env["hr_timesheet.sheet"].search(
                    [
                        ("department_id", "=", rec.id),
                        ("company_id", "!=", rec.company_id.id),
                        ("company_id", "!=", False),
                    ],
                    limit=1,
                )
            ]:
                if (
                    rec.company_id
                    and field.company_id
                    and rec.company_id != field.company_id
                ):
                    raise ValidationError(
                        _(
                            "You cannot change the company, as this"
                            " %(rec_name)s (%(rec_display_name)s) is assigned"
                            " to %(current_name)s (%(current_display_name)s).",
                            rec_name=rec._name,
                            rec_display_name=rec.display_name,
                            current_name=field._name,
                            current_display_name=field.display_name,
                        )
                    )
