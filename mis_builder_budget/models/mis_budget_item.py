# Copyright 2017 ACSONE SA/NV
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import api, fields, models


class MisBudgetItem(models.Model):
    _inherit = ["mis.budget.item.abstract", "mis.kpi.data"]
    _name = "mis.budget.item"
    _description = "MIS Budget Item (by KPI)"
    _order = "budget_id, date_from, seq1, seq2"

    budget_id = fields.Many2one(comodel_name="mis.budget")
    report_id = fields.Many2one(related="budget_id.report_id")
    kpi_expression_id = fields.Many2one(
        domain=(
            "[('kpi_id.report_id', '=', report_id),"
            " ('kpi_id.budgetable', '=', True)]"
        )
    )

    company_id = fields.Many2one(
        comodel_name="res.company",
        compute="_compute_company_id",
        store=True,
        readonly=False,
    )
    budget_company_id = fields.Many2one(
        string="#Technical field: Budget Company", related="budget_id.company_id"
    )

    @api.depends("budget_id.company_id")
    def _compute_company_id(self):
        for rec in self:
            rec.company_id = rec.budget_id.company_id

    def _prepare_overlap_domain(self):
        """Prepare a domain to check for overlapping budget items."""
        domain = super()._prepare_overlap_domain()
        domain.extend(
            [
                ("kpi_expression_id", "=", self.kpi_expression_id.id),
                ("company_id", "=", self.company_id.id),
            ]
        )
        return domain

    @api.constrains(
        "date_range_id",
        "date_from",
        "date_to",
        "budget_id",
        "kpi_expression_id",
        "company_id",
    )
    def _check_dates(self):
        super()._check_dates()
        return
