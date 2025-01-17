/* Copyright 2025 Patryk Pyczko (APSL-Nagarro)<ppyczko@apsl.net>
 * License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl). */

odoo.define("website_sale_order_cancel.cancel_order_tour", function (require) {
    "use strict";

    var tour = require("web_tour.tour");

    tour.register(
        "sale_order_cancel_tour",
        {
            url: "/my/orders/8",
            test: true,
        },
        [
            // Step 1: Locate and click the Cancel button to initiate the cancellation process
            {
                trigger: "#cancelOrderButton",
                content:
                    "Click on the Cancel button to start the cancellation process.",
                run: "click",
            },

            // Step 2: Locate the 'Submit' button in the cancellation modal and confirm the cancellation
            {
                trigger: "#submit_cancel_button",
                content:
                    "Submit the cancellation form to confirm the order cancellation.",
                run: "click",
            },
        ]
    );
});
