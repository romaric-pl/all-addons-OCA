# Copyright 2024 Tecnativa - David Vidal
# License AGPL-3 - See https://www.gnu.org/licenses/agpl-3.0.html

from odoo import api, models


class ProductProduct(models.Model):
    _inherit = "product.product"

    @api.model
    def search(self, args, offset=0, limit=None, order=None, count=False):
        dom = self.env["multi.company.abstract"]._patch_company_domain(args)
        return super().search(dom, offset=offset, limit=limit, order=order, count=count)
