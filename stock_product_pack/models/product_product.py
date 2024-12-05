# Copyright 2019 Tecnativa - Ernesto Tejeda
# Copyright 2020 Tecnativa - João Marques
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

import math

from odoo import models


class ProductProduct(models.Model):
    _inherit = "product.product"

    def _compute_quantities_dict(
        self, lot_id, owner_id, package_id, from_date=False, to_date=False
    ):
        packs = self.filtered("pack_ok")
        subproducts = packs.pack_line_ids.filtered(
            lambda p: p.product_id.detailed_type == "product"
        ).mapped("product_id")
        res = super(ProductProduct, self | subproducts)._compute_quantities_dict(
            lot_id, owner_id, package_id, from_date=from_date, to_date=to_date
        )
        for pack in packs.with_context(prefetch_fields=False):
            pack_qty_available = []
            pack_virtual_available = []
            pack_free_qty = []

            for line in pack.pack_line_ids.filtered(
                lambda p: p.product_id.detailed_type == "product"
            ):
                sub_qty = line.quantity
                if sub_qty:
                    pack_qty_available.append(
                        math.floor(
                            (
                                res[line.product_id.id]["qty_available"]
                                - res[line.product_id.id]["outgoing_qty"]
                            )
                            / sub_qty
                        )
                    )
                    pack_virtual_available.append(
                        math.floor(
                            res[line.product_id.id]["virtual_available"] / sub_qty
                        )
                    )
                    pack_free_qty.append(
                        math.floor(res[line.product_id.id]["free_qty"] / sub_qty)
                    )
            res[pack.id] = {
                "qty_available": (pack_qty_available and min(pack_qty_available) or 0),
                "free_qty": (pack_free_qty and min(pack_free_qty) or 0),
                "incoming_qty": 0,
                "outgoing_qty": 0,
                "virtual_available": (
                    pack_virtual_available and min(pack_virtual_available) or 0
                ),
            }
        return res

    def _compute_quantities(self):
        """In v13 Odoo introduces a filter for products not services.
        To keep how it was working on v12 we try to get stock for
        service products if they are pack.
        """
        service_pack_products = self.filtered(
            lambda p: p.detailed_type == "service" and p.pack_ok
        )
        result = super(
            ProductProduct, self - service_pack_products
        )._compute_quantities()
        res = service_pack_products._compute_quantities_dict(
            self._context.get("lot_id"),
            self._context.get("owner_id"),
            self._context.get("package_id"),
            self._context.get("from_date"),
            self._context.get("to_date"),
        )
        for product in service_pack_products:
            product.qty_available = res[product.id]["qty_available"]
            product.incoming_qty = res[product.id]["incoming_qty"]
            product.outgoing_qty = res[product.id]["outgoing_qty"]
            product.virtual_available = res[product.id]["virtual_available"]
            product.free_qty = res[product.id]["free_qty"]
        return result
