# Copyright 2021 Camptocamp SA
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl)

import re

from odoo.addons.delivery_postlogistics.postlogistics import web_service

UNNUMBER_REGEX = re.compile("^[0-9]{1,4}")


class PostlogisticsWebServiceDangerousGoods(web_service.PostlogisticsWebService):
    def _get_unnumbers(self, picking, pack=None):
        """
        If any dangerous goods with limited quantity, returns a list of UNNumbers.
        """
        products = (
            pack
            and pack.mapped("quant_ids.product_id")
            or picking.mapped("move_lines.product_id")
        )
        limited_amount_lq = picking.env.ref(
            "l10n_eu_product_adr_dangerous_goods.limited_amount_1"
        )
        limited_quantity_products = products.filtered(
            lambda p: p.is_dangerous and p.limited_amount_id == limited_amount_lq
        )
        # Since 14.0, un numbers checks are done directly in l10n_eu_product_adr
        return [
            int(product.adr_goods_id.un_number) for product in limited_quantity_products
        ]

    def _prepare_attributes(
        self, picking, pack=None, pack_num=None, pack_total=None, pack_weight=None
    ):
        # Adds a new attribute UNNumbers when there's dangerous goods
        # in the pack / picking
        res = super()._prepare_attributes(
            picking, pack, pack_num, pack_total, pack_weight
        )
        unnumbers = self._get_unnumbers(picking, pack)
        if unnumbers:
            res.setdefault("przl", []).append("LQ")
            res["unnumbers"] = unnumbers
        return res
