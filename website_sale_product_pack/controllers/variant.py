from odoo.http import request

from odoo.addons.website_sale.controllers.variant import WebsiteSaleVariantController


class WebsiteSaleVariantController(WebsiteSaleVariantController):
    def get_combination_info_website(
        self,
        product_template_id,
        product_id,
        combination,
        add_qty,
        parent_combination=None,
        **kwargs,
    ):
        request.update_context(whole_pack_price=True)
        return super().get_combination_info_website(
            product_template_id,
            product_id,
            combination,
            add_qty,
            parent_combination=parent_combination,
            **kwargs,
        )
