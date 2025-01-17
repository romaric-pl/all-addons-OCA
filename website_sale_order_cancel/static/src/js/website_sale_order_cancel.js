/* Copyright 2025 Patryk Pyczko (APSL-Nagarro)<ppyczko@apsl.net>
 * License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl). */

odoo.define("website_sale_order_cancel_widget", function (require) {
    "use strict";

    const publicWidget = require("web.public.widget");
    const Dialog = require("web.Dialog");

    var WebsiteSaleOrderCancelWidget = publicWidget.Widget.extend({
        selector: ".cancelOrderForm",
        events: {
            "click #submit_cancel_button": "_onSubmit",
        },

        _onSubmit: function (e) {
            e.preventDefault();
            var sale_order_id = this.$("#sale_order_id").val();

            fetch("/cancel/confirm", {
                method: "POST",
                headers: {
                    "Content-Type": "application/json",
                },
                body: JSON.stringify({sale_order_id: sale_order_id}),
            })
                .then((response) => response.json())
                .then((data) => {
                    if (data.result.success) {
                        location.reload();
                    } else {
                        this._showDialog("Error", "Unable to cancel the order.");
                    }
                })
                .catch(() =>
                    this._showDialog("Error", "An unexpected error occurred.")
                );
        },

        _showDialog(title, message) {
            Dialog.alert(this, message, {title});
        },
    });

    publicWidget.registry.WebsiteSaleOrderCancel = WebsiteSaleOrderCancelWidget;

    return WebsiteSaleOrderCancelWidget;
});
