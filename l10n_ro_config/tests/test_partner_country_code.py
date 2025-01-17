# Copyright (C) 2015 Forest and Biomass Romania
# Copyright (C) 2020 NextERP Romania
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from odoo.tests import Form, tagged

from odoo.addons.account.tests.common import AccountTestInvoicingCommon


@tagged("post_install", "-at_install")
class TestPartnerVATSubjected(AccountTestInvoicingCommon):
    @classmethod
    def setUpClass(cls):
        super().setUpClass(chart_template_ref="ro")
        cls.mainpartner = cls.env.ref("base.main_partner")
        cls.env.company.anglo_saxon_accounting = True
        cls.env.company.l10n_ro_accounting = True


@tagged("post_install", "-at_install")
class TestPartnerVAT(TestPartnerVATSubjected):
    def test_onchange_l10n_ro_vat_subjected(self):
        """Check onchange vat subjected and country."""
        # test setting l10n_ro_vat_subjected as True
        self.mainpartner.vat = "4264242"
        self.mainpartner.country_id = self.env.ref("base.ro")
        self.mainpartner.l10n_ro_vat_subjected = True
        self.mainpartner.onchange_l10n_ro_vat_subjected()
        # Test setting l10n_ro_vat_subjected as False
        self.assertEqual(self.mainpartner.vat, "RO4264242")
        self.mainpartner.l10n_ro_vat_subjected = False
        self.mainpartner.onchange_l10n_ro_vat_subjected()
        self.assertEqual(self.mainpartner.vat, "4264242")
        # Check split vat with no country code in vat
        (
            vat_country,
            l10n_ro_vat_number,
        ) = self.mainpartner._split_vat_and_mapped_country(self.mainpartner.vat)
        self.assertEqual(vat_country, "ro")
        self.assertEqual(l10n_ro_vat_number, "4264242")

    def test_form_partner(self):
        test_company = self.env["res.company"].create(
            {
                "name": "Test Company",
            }
        )
        partner = self.env["res.partner"].create(
            {
                "name": "Test Partner",
                "is_company": True,
            }
        )

        partner_form = Form(partner)
        partner_form.name = "Test Partner"
        partner_form.l10n_ro_vat_subjected = True

        self.env.company = test_company
        partner_form = Form(partner)
        partner_form.name = "Test Partner"
        with self.assertRaises(AssertionError):
            partner_form.l10n_ro_vat_subjected = True
