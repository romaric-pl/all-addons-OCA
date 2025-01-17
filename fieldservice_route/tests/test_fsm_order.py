# Copyright (C) 2019 Open Source Integrators
# Copyright (C) 2019 Serpent consulting Services
# Copyright 2022 Tecnativa - Víctor Martínez
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

from datetime import datetime, timedelta

from odoo.tests import Form, common


class FSMOrderRouteCase(common.TransactionCase):
    def setUp(self):
        super().setUp()
        self.fsm_stage_obj = self.env["fsm.stage"]
        self.fsm_order_obj = self.env["fsm.order"]
        self.fsm_route_obj = self.env["fsm.route"]
        self.fsm_dayroute_obj = self.env["fsm.route.dayroute"]
        self.test_person = self.env.ref("fieldservice.test_person")
        self.person_1 = self.env.ref("fieldservice.person_1")
        self.test_location = self.env.ref("fieldservice.test_location")
        self.stage_completed = self.env.ref("fieldservice.fsm_stage_completed")
        date = datetime.now()
        self.date = date.replace(microsecond=0)
        self.days = [
            self.env.ref("fieldservice_route.fsm_route_day_0").id,
            self.env.ref("fieldservice_route.fsm_route_day_1").id,
            self.env.ref("fieldservice_route.fsm_route_day_2").id,
            self.env.ref("fieldservice_route.fsm_route_day_3").id,
            self.env.ref("fieldservice_route.fsm_route_day_4").id,
            self.env.ref("fieldservice_route.fsm_route_day_5").id,
            self.env.ref("fieldservice_route.fsm_route_day_6").id,
        ]
        self.fsm_route_id = self.fsm_route_obj.create(
            {
                "name": "Demo Route",
                "max_order": 10,
                "fsm_person_id": self.test_person.id,
                "day_ids": [(6, 0, self.days)],
            }
        )
        self.test_location.fsm_route_id = self.fsm_route_id.id

        self.dayroute_today = self.fsm_dayroute_obj.create(
            {
                "name": "Today Day Route",
                "route_id": self.fsm_route_id.id,
                "date": self.date.date(),
                "person_id": self.test_person.id,
            }
        )
        self.dayroute_future = self.fsm_dayroute_obj.create(
            {
                "name": "Future Day Route",
                "route_id": self.fsm_route_id.id,
                "date": (self.date + timedelta(days=1)).date(),
                "person_id": self.test_person.id,
            }
        )
        self.dayroute_past = self.fsm_dayroute_obj.create(
            {
                "name": "Past Day Route",
                "route_id": self.fsm_route_id.id,
                "date": (self.date - timedelta(days=1)).date(),
                "person_id": self.test_person.id,
            }
        )

        self.active_order = self.fsm_order_obj.create(
            {
                "location_id": self.test_location.id,
                "fsm_route_id": self.fsm_route_id.id,
                "dayroute_id": self.dayroute_today.id,
                "person_id": self.test_person.id,
                "scheduled_date_start": self.date,
            }
        )
        self.closed_order = self.fsm_order_obj.create(
            {
                "location_id": self.test_location.id,
                "fsm_route_id": self.fsm_route_id.id,
                "dayroute_id": self.dayroute_today.id,
                "person_id": self.test_person.id,
                "stage_id": self.stage_completed.id,
                "scheduled_date_start": self.date,
            }
        )

    def test_create_day_route(self):
        order_form = Form(self.fsm_order_obj)
        order_form.location_id = self.test_location
        order_form.scheduled_date_start = self.date
        order = order_form.save()
        self.assertEqual(order.person_id, self.test_person)
        self.assertEqual(order.fsm_route_id, self.test_location.fsm_route_id)
        self.assertEqual(order.dayroute_id.person_id, order.person_id)
        self.assertEqual(order.dayroute_id.date, order.scheduled_date_start.date())
        self.assertEqual(order.dayroute_id.route_id, order.fsm_route_id)

    def test_write_updates_dayroutes_and_orders(self):
        # Update FSM person on the route
        self.fsm_route_id.write({"fsm_person_id": self.person_1.id})

        # Assert active day routes are updated
        self.assertEqual(self.dayroute_today.person_id, self.person_1)
        self.assertEqual(self.dayroute_future.person_id, self.person_1)

        # Assert past day routes are not updated
        self.assertEqual(self.dayroute_past.person_id, self.test_person)

        # Assert active orders are updated
        self.assertEqual(self.active_order.person_id, self.person_1)

        # Assert closed orders are not updated
        self.assertEqual(self.closed_order.person_id, self.test_person)
