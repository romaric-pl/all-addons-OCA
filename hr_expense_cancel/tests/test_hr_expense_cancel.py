# Copyright 2019 Tecnativa - Ernesto Tejeda
# Copyright 2024 Tecnativa - Víctor Martínez
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo.exceptions import UserError
from odoo.tests.common import Form, tagged

from odoo.addons.hr_expense.tests.common import TestExpenseCommon


@tagged("-at_install", "post_install")
class TestHrExpenseCancel(TestExpenseCommon):
    @classmethod
    def setUpClass(cls, chart_template_ref=None):
        super().setUpClass(chart_template_ref=chart_template_ref)
        # Create expense + sheet + approve
        expense_form = Form(
            cls.env["hr.expense"].with_context(
                default_product_id=cls.product_a.id,
                default_employee_id=cls.expense_employee.id,
            )
        )
        expense_form.name = "Test expense"
        cls.expense = expense_form.save()
        res = cls.expense.action_submit_expenses()
        sheet_form = Form(cls.env[res["res_model"]].with_context(**res["context"]))
        cls.expense_sheet = sheet_form.save()
        cls.expense_sheet.approve_expense_sheets()

    def _get_payment_wizard(self):
        res = self.expense_sheet.action_register_payment()
        register_form = Form(self.env[res["res_model"]].with_context(**res["context"]))
        register_form.journal_id = self.company_data["default_journal_bank"]
        register_form.amount = self.expense_sheet.total_amount
        return register_form.save()

    def test_action_cancel_posted(self):
        self.expense_sheet.action_sheet_move_create()
        self.assertFalse(len(self.expense_sheet.payment_ids), 1)
        self.assertTrue(self.expense_sheet.account_move_id)
        self.expense_sheet.action_cancel()
        self.assertFalse(self.expense_sheet.payment_ids)
        self.assertFalse(self.expense_sheet.account_move_id)

    def test_action_cancel_no_update_posted(self):
        journals = (
            self.company_data["default_journal_bank"]
            | self.company_data["default_journal_purchase"]
        )
        journals.write({"restrict_mode_hash_table": True})
        self.test_action_cancel_company_account()
        with self.assertRaises(UserError):
            self.test_action_cancel_own_account()

    def test_action_cancel_company_account(self):
        self.expense.payment_mode = "company_account"
        self.expense_sheet.action_sheet_move_create()
        self.assertTrue(self.expense_sheet.account_move_id)
        self.expense_sheet.action_cancel()
        self.assertFalse(self.expense_sheet.account_move_id)

    def test_action_cancel_own_account(self):
        self.expense_sheet.action_sheet_move_create()
        payment_wizard = self._get_payment_wizard()
        payment_wizard.action_create_payments()
        self.assertTrue(self.expense_sheet.payment_ids)
        self.expense_sheet.action_cancel()  # assertFalse(payment.exist)
        self.assertFalse(self.expense_sheet.payment_ids.state != "cancel")
