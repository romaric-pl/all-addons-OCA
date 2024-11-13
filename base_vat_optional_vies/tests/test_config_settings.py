# Copyright 2024 Moduon Team S.L.
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from unittest import mock

from odoo.tests import common
from odoo.tools import mute_logger


class TestConfigSettings(common.TransactionCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.partner1, cls.partner2 = (
            cls.env["res.partner"]
            .with_context(no_vat_validation=True)
            .create(
                [
                    {
                        "name": "Test partner",
                        "is_company": True,
                        "vat": "ESB87530432",
                        "country_id": cls.env.ref("base.es").id,
                    },
                    {
                        "name": "Test partner2",
                        "is_company": True,
                        "vat": "ES00000000T",
                        "country_id": cls.env.ref("base.es").id,
                    },
                ]
            )
        )
        cls.config = cls.env["res.config.settings"].create({"vat_check_vies": True})

    def setUp(self):
        super().setUp()
        self.mock_check_vies = self.startPatcher(
            mock.patch(
                "odoo.addons.base_vat.models.res_partner.check_vies",
                side_effect=(lambda vat: {"valid": vat == "ESB87530432"}),
            )
        )

    @mute_logger(
        "odoo.addons.base_vat_optional_vies.models.res_config_settings",
        "odoo.addons.base_vat.models.res_partner",
    )
    def test_batch_checking(self):
        self.config.execute_update_check_vies()
        self.mock_check_vies.assert_any_call("ESB87530432")
        self.mock_check_vies.assert_any_call("ES00000000T")
        self.assertTrue(self.partner1.vies_passed)
        self.assertFalse(self.partner2.vies_passed)
