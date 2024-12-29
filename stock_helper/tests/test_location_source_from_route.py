# Copyright 2022 Michael Tietz (MT Software) <mtietz@mt-software.de>
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl.html).


from .common import StockHelperCommonCase


class TestStockLocationSoruceFromRoute(StockHelperCommonCase):
    def test_get_source_location_from_route(self):
        self.wh.delivery_steps = "pick_pack_ship"
        route = self.wh.delivery_route_id

        location = self.env.ref("stock.stock_location_customers")
        source_location = location._get_source_location_from_route(
            route, "make_to_stock"
        )
        self.assertEqual(source_location, self.wh.lot_stock_id)

        source_location = location._get_source_location_from_route(
            route, "make_to_order"
        )
        self.assertEqual(source_location, self.wh.wh_output_stock_loc_id)

        location = source_location
        source_location = location._get_source_location_from_route(
            route, "make_to_order"
        )
        self.assertEqual(source_location, self.wh.wh_pack_stock_loc_id)

        location = source_location
        source_location = location._get_source_location_from_route(
            route, "make_to_stock"
        )
        self.assertEqual(source_location, self.wh.lot_stock_id)

        location = source_location
        source_location = location._get_source_location_from_route(
            route, "make_to_stock"
        )
        # Since this change in v17
        # https://github.com/odoo/odoo/commit/439ca89a68fe957adbe0f7a6147047593155aa9f
        # _get_rule fallbacks to location's warehouse to check for routes.
        # This makes that the receipt route is found by _get_source_location_from_route.
        # However, this is the case only with `stock` module installed, because
        # as soon as `mrp` or `purchase` is installed that first step of the receipt
        # route get removed in favor of manufacture or purchase routes. See
        # https://github.com/odoo/odoo/commit/d25d320e0e870980971de945719f7b7d5deadd3c
        if hasattr(self.wh, "manufacture_to_resupply") or hasattr(
            self.wh, "buy_to_resupply"
        ):
            expected_location = self.env["stock.location"].browse()
        else:  # only `stock` installed.
            expected_location = self.supplier_loc
        self.assertEqual(source_location, expected_location)
