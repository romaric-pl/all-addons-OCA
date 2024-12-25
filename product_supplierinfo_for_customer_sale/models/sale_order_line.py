# Copyright 2013-2017 Agile Business Group sagl
#     (<http://www.agilebg.com>)
# Copyright 2021 ForgeFlow S.L. (https://www.forgeflow.com)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from odoo import api, fields, models


class SaleOrderLine(models.Model):
    _inherit = "sale.order.line"

    product_customer_code = fields.Char(
        compute="_compute_product_customer_code",
        string="Product Customer Code",
        search="_search_product_customer_code",
    )
    product_customer_name = fields.Char(
        compute="_compute_product_customer_code",
        string="Product Customer Name",
        search="_search_product_customer_name",
    )

    @api.depends("order_id.partner_id", "product_id", "company_id")
    def _compute_product_customer_code(self):
        for line in self:
            product_customer_name = product_customer_code = False

            if line.product_id and line.order_id and line.order_id.partner_id:
                customerinfo = line.product_id._select_customerinfo(
                    partner=line.order_partner_id,
                    quantity=None,
                )
                product_customer_code = customerinfo.product_code
                product_customer_name = customerinfo.product_name

            line.product_customer_code = product_customer_code
            line.product_customer_name = product_customer_name

    def _search_product_customer_code(self, operator, value):
        return [
            ("product_id.customer_ids.product_code", operator, value),
            (
                "order_id.partner_id",
                "=",
                self.env["product.customerinfo"]
                .search([("product_code", operator, value)])
                .name.id,
            ),
        ]

    def _search_product_customer_name(self, operator, value):
        return [
            ("product_id.customer_ids.product_name", operator, value),
            (
                "order_id.partner_id",
                "=",
                self.env["product.customerinfo"]
                .search([("product_name", operator, value)])
                .name.id,
            ),
        ]

    @api.onchange("product_id")
    def product_id_change(self):
        result = super(SaleOrderLine, self).product_id_change()
        for line in self.filtered(
            lambda sol: sol.product_id.product_tmpl_id.customer_ids
            and sol.order_id.pricelist_id.item_ids
        ):
            product = line.product_id
            items = self.env["product.pricelist.item"].search(
                [
                    ("pricelist_id", "=", line.order_id.pricelist_id.id),
                    ("compute_price", "=", "formula"),
                    ("base", "=", "partner"),
                    "|",
                    ("applied_on", "=", "3_global"),
                    "|",
                    "&",
                    ("categ_id", "=", product.categ_id.id),
                    ("applied_on", "=", "2_product_category"),
                    "|",
                    "&",
                    ("product_tmpl_id", "=", product.product_tmpl_id.id),
                    ("applied_on", "=", "1_product"),
                    "&",
                    ("product_id", "=", product.id),
                    ("applied_on", "=", "0_product_variant"),
                ]
            )
            if items:
                supplierinfo = line.product_id._select_customerinfo(
                    partner=line.order_partner_id, quantity=None
                )
                if supplierinfo and supplierinfo.min_qty:
                    line.product_uom_qty = supplierinfo.min_qty
        return result
