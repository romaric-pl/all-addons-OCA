# Copyright 2017 Akretion (http://www.akretion.com).
# @author Sébastien BEAU <sebastien.beau@akretion.com>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import fields
from odoo.tests.common import TransactionCase
from odoo.tools import float_compare

from odoo.addons.sale_promotion_rule.tests.test_promotion import (
    FIXED_AMOUNT_CODE,
    AbstractCommonPromotionCase,
)


class TestSaleOrder(TransactionCase, AbstractCommonPromotionCase):
    def setUp(self, *args, **kwargs):
        super().setUp(*args, **kwargs)
        self.set_up("sale_promotion_rule.sale_order_promotion")

    def test_discount_amount(self):
        self.assertTrue(self.promotion_rule_fixed_amount.discount_amount > 0)
        price_total_no_discount = self.sale.price_total_no_discount
        amount_total = self.sale.amount_total
        self.assertTrue(price_total_no_discount > 0)
        self.assertEqual(price_total_no_discount, amount_total)
        self.promotion_rule_auto.minimal_amount = 999999999  # disable
        self.promotion_rule_fixed_amount.discount_type = "amount_tax_included"
        # we apply a discount of 20 on untaxed amount
        self.add_coupon_code(FIXED_AMOUNT_CODE)
        self.assertEqual(
            0,
            float_compare(
                self.sale.discount_total,
                self.env.user.company_id.currency_id._convert(
                    self.promotion_rule_fixed_amount.discount_amount,
                    self.sale.currency_id,
                    self.sale.company_id,
                    fields.Date.today(),
                ),
                precision_digits=self.price_precision_digits,
            ),
            "%s != %s"
            % (
                self.sale.discount_total,
                self.promotion_rule_fixed_amount.discount_amount,
            ),
        )
        # check that the price total without discount is equal to the amount
        # total before applying the discount.
        self.assertEqual(amount_total, self.sale.price_total_no_discount)
        self.assertEqual(
            self.sale.amount_total + self.sale.discount_total,
            self.sale.price_total_no_discount,
        )
