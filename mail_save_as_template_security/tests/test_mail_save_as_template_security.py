# Copyright 2024 Alberto Martínez <alberto.martinez@sygel.es>
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from lxml import etree

from odoo.tests.common import TransactionCase


class SomethingCase(TransactionCase):
    def setUp(self):
        super().setUp()

    def test_fields_view_get(self):
        # Test view with admin user
        view = (
            self.env["mail.compose.message"]
            .with_user(self.env.ref("base.user_admin"))
            .fields_view_get(view_type="form")
        )
        buttons = etree.fromstring(view["arch"]).xpath(
            "//button[@name='action_save_as_template']"
        )
        self.assertTrue(buttons, "Wrong Xpath")
        self.assertIsNone(buttons[0].get("invisible"))
        # Test view with demo user. Button should be invisible
        view = (
            self.env["mail.compose.message"]
            .with_user(self.env.ref("base.user_demo"))
            .fields_view_get(view_type="form")
        )
        buttons = etree.fromstring(view["arch"]).xpath(
            "//button[@name='action_save_as_template']"
        )
        self.assertTrue(buttons, "Wrong Xpath")
        self.assertTrue(buttons[0].get("invisible"))
