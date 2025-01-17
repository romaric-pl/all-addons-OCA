from odoo.tests import common


class TestSaleCouponFreeShippingDefaultProduct(common.SavepointCase):
    @classmethod
    def setUpClass(cls):

        super(TestSaleCouponFreeShippingDefaultProduct, cls).setUpClass()

        cls.coupon_program_model = cls.env["coupon.program"]
        cls.product_model = cls.env["product.product"]

        # Create a test product for free shipping
        cls.free_shipping_product = cls.product_model.create(
            {
                "name": "Free Shipping Product",
                "type": "service",
                "list_price": 0.0,
            }
        )

        # Set the company"s default free shipping product
        cls.env.company.write(
            {"free_shipping_product_default": cls.free_shipping_product.id}
        )

    def test_create_coupon_with_free_shipping(self):
        """Test coupon creation with reward_type set to "free_shipping"."""
        vals = {
            "name": "Free Shipping Test Program",
            "reward_type": "free_shipping",
        }
        program = self.coupon_program_model.create(vals)
        self.assertEqual(
            program.discount_line_product_id.id, self.free_shipping_product.id
        )
