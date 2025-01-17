# Copyright 2025 Patryk Pyczko (APSL-Nagarro)<ppyczko@apsl.net>
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo import http
from odoo.http import request


class SaleOrderCancel(http.Controller):
    @http.route(
        "/cancel/confirm",
        type="json",
        auth="public",
        website=False,
        csrf=False,
        methods=["GET", "POST"],
    )
    def confirm_cancel_sale_order(self):
        """Cancel the sale order after confirmation."""
        sale_order_id = request.jsonrequest.get("sale_order_id")

        if not sale_order_id:
            return {"success": False}

        sale_order = request.env["sale.order"].sudo().browse(int(sale_order_id))
        sale_order.with_context(disable_cancel_warning=True).action_cancel()

        return {
            "success": True,
        }
