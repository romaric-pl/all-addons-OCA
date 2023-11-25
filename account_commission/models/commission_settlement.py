# Copyright 2020 Tecnativa - Manuel Calero
# Copyright 2022 Quartile
# Copyright 2014-2022 Tecnativa - Pedro M. Baeza
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo import _, api, fields, models
from odoo.exceptions import UserError
from odoo.tests import Form
from odoo.tools import groupby


class CommissionSettlement(models.Model):
    _inherit = "commission.settlement"

    settlement_type = fields.Selection(
        selection_add=[("sale_invoice", "Sales Invoices")],
        ondelete={"sale_invoice": "set default"},
    )
    state = fields.Selection(
        selection_add=[
            ("invoiced", "Invoiced"),
            ("except_invoice", "Invoice exception"),
        ],
        ondelete={"invoiced": "set default", "except_invoice": "set default"},
    )
    invoice_line_ids = fields.One2many(
        comodel_name="account.move.line",
        inverse_name="settlement_id",
        string="Generated invoice lines",
        readonly=True,
    )
    invoice_id = fields.Many2one(
        string="Generated Invoice",
        store=True,
        comodel_name="account.move",
        compute="_compute_invoice_id",
    )

    def _compute_can_edit(self):
        """Make settlements coming from invoice lines to not be editable."""
        sale_invoices = self.filtered(lambda x: x.settlement_type == "sale_invoice")
        sale_invoices.update({"can_edit": False})
        return super(CommissionSettlement, self - sale_invoices)._compute_can_edit()

    @api.depends("invoice_line_ids")
    def _compute_invoice_id(self):
        for record in self:
            record.invoice_id = record.invoice_line_ids.filtered(
                lambda x: x.parent_state != "cancel"
            )[:1].move_id

    def action_cancel(self):
        """Check if any settlement has been invoiced."""
        if any(x.state != "settled" for x in self):
            raise UserError(_("Cannot cancel an invoiced settlement."))
        return super().action_cancel()

    def action_draft(self):
        self.write({"state": "settled"})

    def unlink(self):
        """Allow to delete only cancelled settlements."""
        if any(x.state == "invoiced" for x in self):
            raise UserError(_("You can't delete invoiced settlements."))
        return super().unlink()

    def action_invoice(self):
        return {
            "type": "ir.actions.act_window",
            "name": _("Make invoice"),
            "res_model": "commission.make.invoice",
            "view_type": "form",
            "target": "new",
            "view_mode": "form",
            "context": {"settlement_ids": self.ids},
        }

    def _get_invoice_partner(self):
        return self[0].agent_id

    def _prepare_invoice(self, journal, product, date=False):
        move_form = Form(
            self.env["account.move"].with_context(default_move_type="in_invoice")
        )
        if date:
            move_form.invoice_date = date
        partner = self._get_invoice_partner()
        move_form.partner_id = partner
        move_form.journal_id = journal
        move_form.currency_id = self.currency_id
        for settlement in self:
            with move_form.invoice_line_ids.new() as line_form:
                line_form.product_id = product
                line_form.quantity = -1 if settlement.total < 0 else 1
                line_form.price_unit = abs(settlement.total)
                # Put period string
                partner = settlement.agent_id
                lang = self.env["res.lang"].search(
                    [
                        (
                            "code",
                            "=",
                            partner.lang or self.env.context.get("lang", "en_US"),
                        )
                    ]
                )
                date_from = fields.Date.from_string(settlement.date_from)
                date_to = fields.Date.from_string(settlement.date_to)
                line_form.name += "\n" + _(
                    "Period: from %(date_from)s to %(date_to)s",
                    date_from=date_from.strftime(lang.date_format),
                    date_to=date_to.strftime(lang.date_format),
                )
                line_form.currency_id = (
                    settlement.currency_id
                )  # todo or compute agent currency_id?\
                line_form.settlement_id = settlement
        vals = move_form._values_to_save(all_fields=True)
        return vals

    def _get_invoice_grouping_keys(self):
        return ["company_id", "currency_id", "agent_id"]

    def make_invoices(self, journal, product, date=False, grouped=False):
        invoice_vals_list = []
        settlement_obj = self.env[self._name]
        if grouped:
            invoice_grouping_keys = self._get_invoice_grouping_keys()
            settlements = groupby(
                self.sorted(
                    key=lambda x: [
                        x._fields[grouping_key].convert_to_write(x[grouping_key], x)
                        for grouping_key in invoice_grouping_keys
                    ],
                ),
                key=lambda x: tuple(
                    x._fields[grouping_key].convert_to_write(x[grouping_key], x)
                    for grouping_key in invoice_grouping_keys
                ),
            )
            grouped_settlements = [
                settlement_obj.union(*list(sett))
                for _grouping_keys, sett in settlements
            ]
        else:
            grouped_settlements = self
        for settlement in grouped_settlements:
            invoice_vals = settlement._prepare_invoice(journal, product, date)
            invoice_vals_list.append(invoice_vals)
        invoices = self.env["account.move"].create(invoice_vals_list)
        invoices.sudo().filtered(lambda m: m.amount_total < 0).with_context(
            include_settlement=True
        ).action_switch_invoice_into_refund_credit_note()
        self.write({"state": "invoiced"})
        return invoices


class SettlementLine(models.Model):
    _inherit = "commission.settlement.line"

    invoice_agent_line_id = fields.Many2one(comodel_name="account.invoice.line.agent")
    invoice_line_id = fields.Many2one(
        comodel_name="account.move.line",
        store=True,
        related="invoice_agent_line_id.object_id",
        string="Source invoice line",
    )

    @api.depends("invoice_agent_line_id")
    def _compute_date(self):
        for record in self.filtered("invoice_agent_line_id"):
            record.date = record.invoice_agent_line_id.invoice_date

    @api.depends("invoice_agent_line_id")
    def _compute_commission_id(self):
        for record in self.filtered("invoice_agent_line_id"):
            record.commission_id = record.invoice_agent_line_id.commission_id

    @api.depends("invoice_agent_line_id")
    def _compute_settled_amount(self):
        for record in self.filtered("invoice_agent_line_id"):
            record.settled_amount = record.invoice_agent_line_id.amount
