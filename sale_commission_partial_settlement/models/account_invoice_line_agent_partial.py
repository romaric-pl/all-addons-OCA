# Copyright 2023 Nextev
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo import fields, models


class AccountInvoiceLineAgentPartial(models.Model):
    _name = "account.invoice.line.agent.partial"
    _description = "Partial agent commissions"

    invoice_line_agent_id = fields.Many2one(
        "account.invoice.line.agent", required=True, ondelete="cascade"
    )
    # logically a One2one
    agent_line = fields.Many2many(
        comodel_name="sale.commission.settlement.line",
        relation="settlement_agent_line_partial_rel",
        column1="agent_line_partial_id",
        column2="settlement_id",
        copy=False,
    )
    account_partial_reconcile_id = fields.Many2one("account.partial.reconcile")
    amount = fields.Monetary(
        string="Commission Amount",
    )
    currency_id = fields.Many2one(
        related="invoice_line_agent_id.currency_id",
    )
