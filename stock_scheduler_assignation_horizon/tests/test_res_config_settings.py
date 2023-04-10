# Copyright 2022 Camptocamp SA
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from datetime import date, timedelta

from odoo.exceptions import ValidationError

from .test_res_config_settings_common import ResConfigSettingsCase


class DeliverySchedulerLimitCase(ResConfigSettingsCase):
    def test_settings_applied_to_company(self):
        self.assertEqual(self.company.is_moves_assignation_limited, True)
        self.assertEqual(self.company.moves_assignation_horizon, 2)

    def test_assignation_horizon_negative_value(self):
        with self.assertRaises(ValidationError) as context:
            self.settings.moves_assignation_horizon = -3
        self.assertEqual(
            "The assignation horizon cannot be negative", str(context.exception)
        )

    def test_delivery_scheduler_horizon_limit(self):
        self.location = self.env.ref("stock.stock_location_stock")
        self.location_dest = self.env.ref("stock.stock_location_customers")

        self.product_1 = self.env["product.product"].create(
            {
                "name": "Test Product 1",
                "type": "product",
            }
        )
        self.env["stock.quant"].with_context(inventory_mode=True).create(
            {
                "product_id": self.product_1.id,
                "location_id": self.location.id,
                "inventory_quantity": 100,
            }
        )

        picking_1 = self._create_picking(days_horizon=1)
        picking_2 = self._create_picking(days_horizon=3)
        picking_1.action_confirm()
        picking_2.action_confirm()

        self.env["procurement.group"].run_scheduler(company_id=self.company.id)

        self.assertEqual(picking_1.state, "assigned")
        self.assertEqual(picking_2.state, "confirmed")

    def _create_picking(self, days_horizon=0):
        scheduled_date = date.today() + timedelta(days=days_horizon)
        operation_type = self.env.ref("stock.picking_type_out")

        return self.env["stock.picking"].create(
            {
                "scheduled_date": scheduled_date,
                "location_id": self.location.id,
                "location_dest_id": self.location_dest.id,
                "picking_type_id": operation_type.id,
                "move_lines": [
                    (
                        0,
                        0,
                        {
                            "name": self.product_1.name,
                            "product_id": self.product_1.id,
                            "product_uom": self.product_1.uom_id.id,
                            "product_uom_qty": 10,
                        },
                    )
                ],
            }
        )
