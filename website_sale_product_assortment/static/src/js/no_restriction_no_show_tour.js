/* Copyright 2021 Tecnativa - Carlos Roca
   License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl). */
odoo.define(
    "website_sale_product_assortment.no_restriction_no_show_tour",
    function (require) {
        "use strict";

        var tour = require("web_tour.tour");

        var steps = [
            {
                trigger: "a:contains('Test Product 1')",
            },
            {
                trigger: "a#add_to_cart",
            },
            {
                trigger: "a[href='/shop/cart']",
                extra_trigger: "sup.my_cart_quantity:contains('1')",
            },
            {
                content: "go back to the store",
                trigger: "a[href='/shop']",
            },
            {
                trigger: "a:contains('Test Product 2')",
            },
            {
                trigger: "a#add_to_cart",
            },
            {
                trigger: "a[href='/shop/cart']",
                extra_trigger: "sup.my_cart_quantity:contains('1')",
            },
        ];

        tour.register(
            "test_assortment_with_no_restriction_no_show",
            {
                url: "/shop",
                test: true,
            },
            steps
        );
        return {
            steps: steps,
        };
    }
);
