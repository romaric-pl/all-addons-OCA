# Copyright 2018 Onestein (<http://www.onestein.eu>)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from odoo import fields
from odoo.exceptions import UserError, ValidationError
from odoo.tests import Form
from odoo.tests.common import TransactionCase


class TestTaxStatementZM(TransactionCase):
    def setUp(self):
        super().setUp()

        self.eur = self.env["res.currency"].search([("name", "=", "EUR")])
        self.coa = self.env.ref("l10n_de_skr03.l10n_de_chart_template", False)
        self.coa = self.coa or self.env.ref(
            "l10n_generic_coa.configurable_chart_template"
        )
        self.company_parent = self.env["res.company"].create(
            {
                "name": "Parent Company",
                "country_id": self.env.ref("base.de").id,
                "currency_id": self.eur.id,
            }
        )
        self.env.user.company_id = self.company_parent
        self.coa.try_loading()
        self.env["l10n.de.tax.statement"].search([("state", "!=", "posted")]).unlink()

        self.tag_1 = self.env["account.account.tag"].create(
            {
                "name": "+81 base",
                "applicability": "taxes",
                "country_id": self.env.ref("base.de").id,
            }
        )
        self.tag_2 = self.env["account.account.tag"].create(
            {
                "name": "+41 base",
                "applicability": "taxes",
                "country_id": self.env.ref("base.de").id,
            }
        )
        self.tag_3 = self.env["account.account.tag"].create(
            {
                "name": "+81 base",
                "applicability": "taxes",
                "country_id": self.env.ref("base.de").id,
            }
        )
        self.tag_4 = self.env["account.account.tag"].create(
            {
                "name": "+21 base",
                "applicability": "taxes",
                "country_id": self.env.ref("base.de").id,
            }
        )

        self.tax_1 = self.env["account.tax"].create({"name": "Tax 1", "amount": 19})
        self.tax_1.invoice_repartition_line_ids[0].tag_ids = self.tag_1
        self.tax_1.invoice_repartition_line_ids[1].tag_ids = self.tag_2

        self.tax_2 = self.env["account.tax"].create({"name": "Tax 2", "amount": 7})
        self.tax_2.invoice_repartition_line_ids[0].tag_ids = self.tag_3
        self.tax_2.invoice_repartition_line_ids[1].tag_ids = self.tag_4

        self.statement_1 = self.env["l10n.de.tax.statement"].create(
            {"name": "Statement 1", "version": "2021"}
        )

    def _create_test_invoice(self, products=True, services=True):
        self.journal_1 = self.env["account.journal"].create(
            {
                "name": "Journal 1",
                "code": "Jou1",
                "type": "sale",
            }
        )
        self.partner = self.env["res.partner"].create({"name": "Test partner"})

        account_receivable = self.env["account.account"].create(
            {
                "user_type_id": self.env.ref("account.data_account_type_expenses").id,
                "code": "EXPTEST",
                "name": "Test expense account",
            }
        )

        invoice_form = Form(
            self.env["account.move"].with_context(default_move_type="out_invoice"),
        )
        invoice_form.partner_id = self.partner
        invoice_form.journal_id = self.journal_1
        invoice_form.invoice_date = fields.Date.today()
        if products:
            with invoice_form.invoice_line_ids.new() as line:
                line.name = "Test line 1"
                line.quantity = 1.0
                line.account_id = account_receivable
                line.price_unit = 100.0
                line.tax_ids.clear()
                line.tax_ids.add(self.tax_1)
        if services:
            with invoice_form.invoice_line_ids.new() as line:
                line.name = "Test line 2"
                line.quantity = 1.0
                line.account_id = account_receivable
                line.price_unit = 50.0
                line.tax_ids.clear()
                line.tax_ids.add(self.tax_2)

        invoice = invoice_form.save()

        if products or services:
            self.assertTrue(len(invoice.line_ids))
        else:
            self.assertFalse(len(invoice.line_ids))

        return invoice

    def test_01_post_final(self):
        self.statement_with_zm = self.env["l10n.de.tax.statement"].create(
            {
                "name": "Statement 1",
                "version": "2021",
            }
        )

        # all previous statements must be already posted
        self.statement_with_zm.statement_update()
        with self.assertRaises(UserError):
            self.statement_with_zm.post()

        self.statement_1.statement_update()
        self.statement_1.post()
        self.assertEqual(self.statement_1.state, "posted")

        # first post
        self.statement_with_zm.post()

        self.assertEqual(self.statement_with_zm.state, "posted")
        self.assertTrue(self.statement_with_zm.date_posted)

        self.statement_with_zm.zm_update()

        # then finalize
        self.statement_with_zm.finalize()
        self.assertEqual(self.statement_with_zm.state, "final")
        self.assertTrue(self.statement_with_zm.date_posted)

        with self.assertRaises(UserError):
            self.statement_with_zm.zm_update()

    def test_02_zm_invoice(self):
        self.statement_1.post()
        self.statement_with_zm = self.env["l10n.de.tax.statement"].create(
            {
                "name": "Statement 1",
                "version": "2021",
            }
        )

        invoice = self._create_test_invoice(services=False)
        invoice.partner_id.country_id = self.env.ref("base.be")
        invoice.action_post()

        self.statement_with_zm.zm_update()
        self.statement_with_zm.post()
        self.assertTrue(self.statement_with_zm.zm_line_ids)
        self.assertTrue(self.statement_with_zm.zm_total)

        for zm_line in self.statement_with_zm.zm_line_ids:
            self.assertTrue(zm_line.amount_products)
            self.assertFalse(zm_line.amount_services)
            amount_products = zm_line.format_amount_products
            self.assertEqual(float(amount_products), zm_line.amount_products)
            amount_services = zm_line.format_amount_services
            self.assertEqual(float(amount_services), zm_line.amount_services)

    def test_03_zm_invoice_service(self):
        self.statement_1.post()
        self.statement_with_zm = self.env["l10n.de.tax.statement"].create(
            {
                "name": "Statement 1",
                "version": "2021",
            }
        )

        invoice = self._create_test_invoice(products=False)
        invoice.partner_id.country_id = self.env.ref("base.be")
        for invoice_line in invoice.invoice_line_ids:
            for tax_line in invoice_line.tax_ids:
                for rep_line in tax_line.invoice_repartition_line_ids:
                    rep_line.tag_ids = self.tag_4
        invoice._onchange_invoice_line_ids()
        invoice.action_post()
        self.statement_with_zm.statement_update()

        self.statement_with_zm.post()
        self.assertTrue(self.statement_with_zm.zm_line_ids)
        self.assertTrue(self.statement_with_zm.zm_total)

        for zm_line in self.statement_with_zm.zm_line_ids:
            self.assertFalse(zm_line.amount_products)
            self.assertTrue(zm_line.amount_services)
            amount_products = zm_line.format_amount_products
            self.assertEqual(float(amount_products), zm_line.amount_products)
            amount_services = zm_line.format_amount_services
            self.assertEqual(float(amount_services), zm_line.amount_services)

    def test_04_zm_invoice_de(self):
        self.statement_1.post()
        self.statement_with_zm = self.env["l10n.de.tax.statement"].create(
            {
                "name": "Statement 1",
                "version": "2021",
            }
        )

        invoice = self._create_test_invoice()
        invoice.partner_id.country_id = self.env.ref("base.de")
        invoice.action_post()

        with self.assertRaises(ValidationError):
            self.statement_with_zm.post()

    def test_05_zm_invoice_outside_europe(self):
        self.statement_1.post()
        self.statement_with_zm = self.env["l10n.de.tax.statement"].create(
            {
                "name": "Statement 1",
                "version": "2021",
            }
        )

        invoice = self._create_test_invoice()
        invoice.partner_id.country_id = self.env.ref("base.us")
        invoice.action_post()

        with self.assertRaises(ValidationError):
            self.statement_with_zm.post()

    def test_06_zm_invoice_download(self):
        self.statement_1.post()
        self.statement_with_zm = self.env["l10n.de.tax.statement"].create(
            {
                "name": "Statement 1",
                "version": "2021",
            }
        )

        invoice = self._create_test_invoice()
        invoice.partner_id.country_id = self.env.ref("base.nl")
        invoice.partner_id.vat = "NL000099998B57"
        invoice.action_post()
        self.statement_with_zm.statement_update()
        self.statement_with_zm.post()

        self.statement_with_zm.zm_download()
