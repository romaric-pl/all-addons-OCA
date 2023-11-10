# Copyright 2022 Tecnativa - Víctor Martínez
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo.tests.common import users

from odoo.addons.sale_report_delivered.tests import test_sale_report_delivered


class TestSaleReportDeliveredBrand(
    test_sale_report_delivered.TestSaleReportDeliveredBase
):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        # Remove this variable in v16 and put instead:
        # from odoo.addons.base.tests.common import DISABLED_MAIL_CONTEXT
        DISABLED_MAIL_CONTEXT = {
            "tracking_disable": True,
            "mail_create_nolog": True,
            "mail_create_nosubscribe": True,
            "mail_notrack": True,
            "no_reset_password": True,
        }
        cls.env = cls.env(context=dict(cls.env.context, **DISABLED_MAIL_CONTEXT))
        cls.brand = cls.env["product.brand"].create({"name": "Test brand"})
        cls.product.product_brand_id = cls.brand
        cls.service.product_brand_id = cls.brand

    @users("admin", "test_user-sale_report_delivered")
    def test_sale_report_delivered_misc(self):
        items = self.env["sale.report.delivered"].search(
            [("order_id", "in", self.orders.ids)]
        )
        self.assertIn(self.brand, items.mapped("product_brand_id"))
