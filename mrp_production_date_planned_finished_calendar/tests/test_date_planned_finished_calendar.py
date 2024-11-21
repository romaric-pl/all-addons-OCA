# Copyright 2024 ForgeFlow S.L. (https://www.forgeflow.com)
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from datetime import date

from odoo import fields
from odoo.tests import Form, TransactionCase


class TestDatePlannedFinished(TransactionCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.env = cls.env(context=dict(cls.env.context, tracking_disable=True))
        cls.company = cls.env.ref("base.main_company")
        cls.warehouse = cls.env.ref("stock.warehouse0")
        cls.calendar = cls.env.ref("resource.resource_calendar_std")
        cls.company.manufacturing_lead = 1
        cls.product = cls.env.ref("mrp.product_product_computer_desk")
        cls.product.produce_delay = 1
        cls.product_bom = cls.env.ref("mrp.mrp_bom_desk")

    def test_mrp_production_date_planned_finished_onchange(self):
        """Test that date_planned_start is set when date_planned_finished
        is changed respecting calendar."""
        with Form(self.env["mrp.production"]) as mo:
            mo.product_id = self.product
            mo.bom_id = self.product_bom
            mo.product_qty = 1
            mo.date_planned_finished = "2024-11-18 10:00:00"  # Monday
        self.assertEqual(
            fields.Date.to_date(mo.date_planned_start), date(2024, 11, 16)
        )  # Saturday
        # Configure calendar in warehouse (Monday to Friday)
        self.warehouse.calendar_id = self.calendar
        with Form(self.env["mrp.production"]) as mo:
            mo.product_id = self.product
            mo.bom_id = self.product_bom
            mo.product_qty = 1
            mo.date_planned_finished = "2024-11-18 10:00:00"  # Monday
        self.assertEqual(
            fields.Date.to_date(mo.date_planned_start), date(2024, 11, 14)
        )  # Thursday
