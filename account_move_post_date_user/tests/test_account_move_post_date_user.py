# Copyright 2024 ForgeFlow S.L.
# License LGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo import fields
from odoo.tests import tagged
from odoo.addons.account.tests.account_test_classes import AccountingTestCase


@tagged("post_install", "-at_install")
class TestAccountMovePostDateUser(AccountingTestCase):
    def setUp(self):
        super(TestAccountMovePostDateUser, self).setUp()
        self.account_move_obj = self.env["account.move"]
        self.partner = self.browse_ref("base.res_partner_12")
        self.user_type_revenue = self.env.ref('account.data_account_type_revenue')
        self.account = self.env['account.account'].create({
            'code': 'NC1114',
            'name': 'Revenue Account',
            'user_type_id': self.user_type_revenue.id,
            'reconcile': True
        })
        self.account2 = self.account_expense = self.env['account.account'].search([
            ('user_type_id', '=', self.env.ref(
                'account.data_account_type_expenses').id)
        ], limit=1)
        self.bank = self.env['res.partner.bank'].create({
            'acc_number': '123456',
            'partner_id': self.env.ref('base.main_partner').id,
            'company_id': self.env.ref('base.main_company').id,
            'bank_id': self.env.ref('base.res_bank_1').id,
        })
        self.journal = self.env['account.journal'].create({
            'name': 'Bank Journal TEST OFX',
            'code': 'BNK12',
            'type': 'bank',
            'bank_account_id': self.bank.id,
        })

        # create a move and post it
        self.move = self.account_move_obj.create(
            {
                "date": fields.Date.today(),
                "journal_id": self.journal.id,
                "line_ids": [
                    (
                        0,
                        0,
                        {
                            "account_id": self.account.id,
                            "credit": 1000.0,
                            "name": "Credit line",
                        },
                    ),
                    (
                        0,
                        0,
                        {
                            "account_id": self.account2.id,
                            "debit": 1000.0,
                            "name": "Debit line",
                        },
                    ),
                ],
            }
        )

    def test_account_move_post_date_user(self):
        self.move.action_post()
        self.assertEqual(self.move.state, "posted")
        self.assertEqual(self.move.last_post_date.date(), fields.Date.today())
        self.assertEqual(self.move.last_post_uid, self.env.user)
