from odoo import _, fields, models
from odoo.exceptions import UserError


class HrTimesheetSheet(models.Model):
    _inherit = "hr_timesheet.sheet"

    purchase_order_id = fields.Many2one("purchase.order", readonly=True)
    allow_generate_purchase_order = fields.Boolean(
        related="employee_id.allow_generate_purchase_order"
    )

    def action_create_purchase_order(self):
        """
        Create Purchase Order
        """
        purchase_order_obj = self.env["purchase.order"].sudo()
        order_count = 0
        group_by_employee = {}
        for record in self:
            group_by_employee.setdefault(record.employee_id, []).append(record)
        for employee, timesheets in group_by_employee.items():
            if any([timesheet.purchase_order_id for timesheet in timesheets]):
                raise UserError(
                    _(
                        "One of the Timesheet Sheets selected for employee {} "
                        "is already related to a PO.",
                    ).format(
                        employee.name,
                    )
                )
            if not employee.allow_generate_purchase_order:
                raise UserError(
                    _(
                        "Employee {} is not enabled for PO creation from Timesheet Sheets."
                    ).format(
                        employee.name,
                    )
                )
            if not employee.billing_partner_id:
                raise UserError(
                    _("Not specified billing partner for the employee: {}.").format(
                        employee.name,
                    )
                )
            if not all([timesheet.state == "done" for timesheet in timesheets]):
                raise UserError(
                    _("Timesheet Sheets must be approved to create a PO from them."),
                )

            order = purchase_order_obj.create(
                {
                    "partner_id": employee.billing_partner_id.id,
                    "order_line": [
                        (
                            0,
                            0,
                            {
                                "product_id": employee.company_id.timesheet_product_id.id,
                                "product_qty": sum(
                                    [timesheet.total_time for timesheet in timesheets]
                                ),
                                "price_unit": employee.timesheet_cost,
                            },
                        )
                    ],
                }
            )
            order_count += 1
            for timesheet in timesheets:
                timesheet.purchase_order_id = order.id
        return {
            "type": "ir.actions.client",
            "tag": "display_notification",
            "params": {
                "type": "success",
                "message": _(
                    "{} POs created from timesheet sheet selected "
                    "for the following employees: {}",
                ).format(
                    order_count,
                    ", ".join([employee.name for employee in group_by_employee.keys()]),
                ),
                "next": {
                    "type": "ir.actions.act_window_close",
                },
            },
        }

    def action_open_purchase_order(self):
        """
        Return action to open related Purchase Order
        """
        self.ensure_one()
        if self.purchase_order_id:
            action = self.env["ir.actions.act_window"]._for_xml_id(
                "purchase.action_rfq_form"
            )
            action["res_id"] = self.purchase_order_id.id
            action["target"] = "current"
            return action

    def action_confirm_purchase_order(self):
        """
        Confirm purchase orders
        """
        self.filtered(lambda rec: rec.purchase_order_id).mapped(
            "purchase_order_id"
        ).sudo().button_confirm()

    def action_timesheet_draft(self):
        sheets_with_po = self.filtered(lambda sheet: sheet.purchase_order_id)
        if sheets_with_po:
            raise UserError(
                _(
                    "Cannot set to draft a Timesheet Sheet from which a PO has been created. "
                    "Please delete the related PO first.",
                ),
            )
        super().action_timesheet_draft()
