# Copyright 2024 Moduon Team S.L.
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl-3.0)

from odoo.tests import tagged

from odoo.addons.account_chart_update.tests.common import TestAccountChartUpdateCommon


@tagged("-at_install", "post_install")
class TestAccountChartUpdate(TestAccountChartUpdateCommon):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        lang_model = cls.env["res.lang"]
        lang_model._activate_lang("en_US")
        lang_model._activate_lang("es_ES")
        lang_model._activate_lang("fr_FR")
        cls.tax_template.with_context(lang="en_US").description = "tax description eng"
        cls.tax_template.with_context(lang="es_ES").name = "tax name es"
        cls.tax_template.with_context(lang="es_ES").description = "tax description es"
        cls.tax_template.with_context(lang="fr_FR").name = "tax name fr"
        cls.tax_template.with_context(lang="fr_FR").description = "tax description fr"

    def test_update_taxes(self):
        wizard = self.wizard_obj.create(self.wizard_vals)
        wizard.action_find_records()
        wizard.action_update_records()
        new_tax = self.env["account.tax"].search(
            [
                ("name", "=", self.tax_template.name),
                ("company_id", "=", self.company.id),
            ]
        )
        self.assertEqual(
            new_tax.with_context(lang="en_US").description, "tax description eng"
        )
        self.assertEqual(new_tax.with_context(lang="es_ES").name, "tax name es")
        self.assertEqual(
            new_tax.with_context(lang="es_ES").description, "tax description es"
        )
        self.assertEqual(new_tax.with_context(lang="fr_FR").name, "tax name fr")
        self.assertEqual(
            new_tax.with_context(lang="fr_FR").description, "tax description fr"
        )

    def test_update_taxes_with_english_deactivate(self):
        # When English is not active the chart update should work also
        self.env["res.partner"].with_context(active_test=False).search([]).write(
            {"lang": "es_ES"}
        )
        self.env["res.users"].with_context(active_test=False).search([]).write(
            {"lang": "es_ES"}
        )
        lang_model = self.env["res.lang"]
        lang_model.search([("code", "=", "en_US")]).write({"active": False})
        self.test_update_taxes()
