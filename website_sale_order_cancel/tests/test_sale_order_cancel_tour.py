# Copyright 2025 Patryk Pyczko (APSL-Nagarro)<ppyczko@apsl.net>
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from datetime import datetime, timedelta

from odoo.tests import HttpCase, TransactionCase, tagged


@tagged("post_install", "-at_install")
class TestSaleOrderCancel(HttpCase, TransactionCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.sale_order = cls.env.ref("sale.sale_order_8")
        cls.sale_order_draft = cls.env.ref("sale.sale_order_1")
        cls.sale_order.write(
            {
                "commitment_date": datetime.now() + timedelta(days=4),
            }
        )

    def test_can_cancel_without_restriction(self):
        self.env["ir.config_parameter"].sudo().set_param(
            "sale.cancel_restrict_days", "0"
        )
        self.sale_order._compute_can_cancel()
        self.assertTrue(
            self.sale_order.can_cancel,
            "Order should be cancellable with no restriction.",
        )

    def test_can_cancel_within_3_day_restriction(self):
        self.env["ir.config_parameter"].sudo().set_param(
            "sale.cancel_restrict_days", "3"
        )
        self.sale_order._compute_can_cancel()
        self.assertTrue(
            self.sale_order.can_cancel,
            "Order should be cancellable within the restriction period.",
        )

    def test_cannot_cancel_after_7_day_restriction(self):
        self.env["ir.config_parameter"].sudo().set_param(
            "sale.cancel_restrict_days", "7"
        )
        self.sale_order._compute_can_cancel()
        self.assertFalse(
            self.sale_order.can_cancel,
            "Order should not be cancellable after the restriction period.",
        )

    def test_tour(self):
        self.assertNotEqual(
            self.sale_order.state,
            "cancel",
            "Sale order shouldn't be cancelled.",
        )

        self.start_tour(
            "/my/orders/8",
            "sale_order_cancel_tour",
            login="demo",
        )

        self.assertEqual(
            self.sale_order.state,
            "cancel",
            "Sale order should be cancelled.",
        )

    def test_no_commitment_or_expected_date(self):
        self.sale_order_draft.write({"commitment_date": False, "expected_date": False})
        self.sale_order_draft._compute_can_cancel()
        self.assertFalse(
            self.sale_order_draft.can_cancel,
            "Order should not be cancellable without a scheduled date.",
        )

    def test_order_not_in_sale_or_done_state(self):
        self.sale_order_draft.write({"state": "draft"})
        self.sale_order_draft._compute_can_cancel()
        self.assertFalse(
            self.sale_order_draft.can_cancel,
            "Order should not be cancellable if not in 'sale' or 'done' state.",
        )
