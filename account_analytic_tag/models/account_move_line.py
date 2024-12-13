from odoo import api, fields, models
from odoo.tools import frozendict


class AccountMoveLine(models.Model):
    _inherit = "account.move.line"

    analytic_tag_ids = fields.Many2many(
        comodel_name="account.analytic.tag",
        string="Analytic Tags",
    )

    @api.depends("analytic_tag_ids")
    def _compute_all_tax(self):
        # Include the analytic tags in the tax move line when applicable
        res = None
        for line in self:
            res = super(AccountMoveLine, line)._compute_all_tax()
            new_compute_all_tax = {}
            for tax_key, tax_vals in line.compute_all_tax.items():
                tax = (
                    self.env["account.tax.repartition.line"]
                    .browse(tax_key.get("tax_repartition_line_id", False))
                    .tax_id
                )
                if tax.analytic:
                    new_key = tax_key.copy()
                    new_key["analytic_tag_ids"] = [
                        (6, 0, [x.id for x in line.analytic_tag_ids])
                    ]
                    tax_key = frozendict(new_key)
                new_compute_all_tax[tax_key] = tax_vals
            line.compute_all_tax = new_compute_all_tax
        return res

    def _prepare_analytic_lines(self):
        """Set tags to the records that have the same or no analytical account."""
        vals = super()._prepare_analytic_lines()
        if self.analytic_tag_ids:
            for val in vals:
                account_id = val.get("account_id")
                tags = self.analytic_tag_ids.filtered(
                    lambda x: not x.account_analytic_id
                    or x.account_analytic_id.id == account_id
                )
                val.update({"tag_ids": [(6, 0, tags.ids)]})
        return vals
