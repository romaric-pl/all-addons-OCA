from odoo import api, models


class CouponProgram(models.Model):
    _inherit = "coupon.program"

    @api.model
    def create(self, vals):
        if vals.get("reward_type") == "free_shipping":
            product = self.env.company.free_shipping_product_default
            if product:
                vals["discount_line_product_id"] = product.id
        program = super(CouponProgram, self).create(vals)

        return program
