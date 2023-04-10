# Copyright 2020 KMEE INFORMATICA LTDA
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import api, fields, models


class ContractContract(models.Model):
    _name = "contract.contract"
    _inherit = [_name, "l10n_br_fiscal.document.mixin"]

    currency_id = fields.Many2one(
        readonly=False,
    )
    country_id = fields.Many2one(related="company_id.country_id", store=True)

    contract_recalculate_taxes_before_invoice = fields.Boolean(
        string="Recalculate taxes before invoicing",
        default="company.contract_recalculate_taxes_before_invoice",
    )

    @api.model
    def _fiscal_operation_domain(self):
        domain = [("state", "=", "approved")]
        return domain

    @api.model
    def default_get(self, fields_list):
        vals = super().default_get(fields_list)
        contract_type = vals.get("contract_type")
        if contract_type:
            company_id = vals.get("company_id")
            if company_id:
                company_id = self.env["res.company"].browse(company_id)
            else:
                company_id = self.env.user.company_id
            if contract_type == "sale":
                fiscal_operation_id = company_id.contract_sale_fiscal_operation_id
            else:
                fiscal_operation_id = company_id.contract_purchase_fiscal_operation_id
            vals.update(
                {
                    "fiscal_operation_id": fiscal_operation_id.id,
                }
            )
        return vals

    cnpj_cpf = fields.Char(
        string="CNPJ/CPF",
        related="partner_id.cnpj_cpf",
    )

    legal_name = fields.Char(
        string="Legal Name",
        related="partner_id.legal_name",
    )

    ie = fields.Char(
        string="State Tax Number/RG",
        related="partner_id.inscr_est",
    )

    fiscal_operation_id = fields.Many2one(
        comodel_name="l10n_br_fiscal.operation",
        string="Fiscal Operation",
        domain=lambda self: self._fiscal_operation_domain(),
    )

    comment_ids = fields.Many2many(
        comodel_name="l10n_br_fiscal.comment",
        relation="contract_comment_rel",
        column1="contract_id",
        column2="comment_id",
        string="Comments",
    )

    def _get_amount_lines(self):
        """Get object lines instaces used to compute fields"""
        return self.mapped("contract_line_ids")

    @api.depends("contract_line_ids")
    def _compute_amount(self):
        super()._compute_amount()

    def _prepare_invoice(self, date_invoice, journal=None):
        self.ensure_one()
        invoice_vals = self._prepare_br_fiscal_dict()
        invoice_vals.update(super()._prepare_invoice(date_invoice, journal))
        return invoice_vals

    @api.model
    def _finalize_invoice_creation(self, invoices):
        super()._finalize_invoice_creation(invoices)

        for invoice in invoices:
            invoice.fiscal_document_id._onchange_document_serie_id()
            invoice.fiscal_document_id._onchange_company_id()

            for line in invoice.invoice_line_ids:
                name = line.name
                price = line.contract_line_id.price_unit
                line._onchange_product_id_fiscal()
                line.name = name
                line.price_unit = price
                line._onchange_fiscal_operation_id()
                line._onchange_fiscal_tax_ids()
                line.price_unit = price

            invoice._onchange_invoice_line_ids()

    def _prepare_recurring_invoices_values(self, date_ref=False):
        """
        Overwrite contract method to verify and create invoices according to
        the Fiscal Operation of each contract line
        :return: list of dictionaries (inv_ids)
        """
        invoices_values = super()._prepare_recurring_invoices_values(date_ref=date_ref)

        if not isinstance(invoices_values, list):
            invoices_values = [invoices_values]

        inv_vals = []
        document_type_list = []

        for invoice_val in invoices_values:

            if not invoice_val.get("fiscal_operation_id"):
                invoice_val["document_type_id"] = False
                inv_vals.append(invoice_val)
            else:
                # Identify how many Document Types exist
                for inv_line in invoice_val.get("invoice_line_ids"):

                    company = self.env["res.company"].browse(
                        inv_line[2].get("company_id")
                    )

                    if type(inv_line[2]) == list:
                        continue

                    operation_line_id = self.env[
                        "l10n_br_fiscal.operation.line"
                    ].browse(inv_line[2].get("fiscal_operation_line_id"))

                    fiscal_document_type = operation_line_id.get_document_type(company)

                    if fiscal_document_type.id not in document_type_list:
                        document_type_list.append(fiscal_document_type.id)
                        inv_to_append = invoice_val.copy()
                        inv_to_append["invoice_line_ids"] = [inv_line]
                        inv_to_append["document_type_id"] = fiscal_document_type.id
                        inv_to_append["document_serie_id"] = (
                            self.env["l10n_br_fiscal.document.serie"]
                            .search(
                                [
                                    (
                                        "document_type_id",
                                        "=",
                                        inv_to_append["document_type_id"],
                                    ),
                                    ("company_id", "=", company.id),
                                ],
                                limit=1,
                            )
                            .id
                        )
                        inv_vals.append(inv_to_append)
                    else:
                        index = document_type_list.index(fiscal_document_type.id)
                        inv_vals[index]["invoice_line_ids"].append(inv_line)

        if inv_vals:
            invoice_values = inv_vals

        return invoice_values
