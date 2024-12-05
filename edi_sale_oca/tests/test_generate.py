# Copyright 2024 Camptocamp SA
# @author: Simone Orsi <simahawk@gmail.com>
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).


from odoo.addons.component.tests.common import SavepointComponentRegistryCase
from odoo.addons.edi_oca.tests.common import EDIBackendTestMixin
from odoo.addons.edi_oca.tests.fake_components import (
    FakeOutputGenerator,
    FakeOutputSender,
)


class Generator(FakeOutputGenerator):
    _backend_type = "sale_demo"
    _exchange_type = "demo_SaleOrder_out"


class Sender(FakeOutputSender):
    _backend_type = "sale_demo"
    _exchange_type = "demo_SaleOrder_out"


class TestProcessComponent(SavepointComponentRegistryCase, EDIBackendTestMixin):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls._setup_env()
        cls.backend = cls._get_backend()
        cls.exc_type = cls.env.ref("edi_sale_oca.demo_edi_exc_type_order_out")
        cls.edi_conf_confirmed = cls.env.ref(
            "edi_sale_oca.demo_edi_configuration_confirmed"
        )
        cls.edi_conf_done = cls.env.ref("edi_sale_oca.demo_edi_configuration_done")
        cls.partner = cls.env.ref("base.res_partner_2").copy({"name": "John Doe"})
        cls._load_module_components(cls, "edi_oca")
        cls._load_module_components(cls, "edi_sale_oca")
        cls._build_components(
            cls,
            Generator,
            Sender,
        )

    def setUp(self):
        super().setUp()
        Generator.reset_faked()
        Sender.reset_faked()

    @classmethod
    def _get_backend(cls):
        return cls.env.ref("edi_sale_oca.demo_edi_backend")

    def test_lookup(self):
        # Just ensuring test setup is done properly
        record = self.backend.create_record(self.exc_type.code, {})
        comp = self.backend._get_component(record, "generate")
        self.assertEqual(comp._name, Generator._name)
        comp = self.backend._get_component(record, "send")
        self.assertEqual(comp._name, Sender._name)

    def test_new_order_no_conf_no_output(self):
        order = self.env["sale.order"].create(
            {
                "partner_id": self.partner.id,
            }
        )
        order.action_confirm()
        self.assertFalse(order.exchange_record_ids)

    def test_new_order_1conf_output(self):
        self.partner.edi_sale_conf_ids = self.edi_conf_confirmed
        order = self.env["sale.order"].create(
            {
                "partner_id": self.partner.id,
            }
        )
        self.assertFalse(order.exchange_record_ids)
        order.with_context(fake_output="ORDER CONFIRM").action_confirm()
        self.assertEqual(len(order.exchange_record_ids), 1)
        record = order.exchange_record_ids[0]
        self.assertEqual(record._get_file_content(), "ORDER CONFIRM")
        self.assertEqual(record.type_id, self.exc_type)
        # When done, nothing changes
        order.action_done()
        self.assertEqual(len(order.exchange_record_ids), 1)
        record = order.exchange_record_ids[0]
        self.assertEqual(record.type_id, self.exc_type)

    def test_new_order_2conf_output(self):
        self.partner.edi_sale_conf_ids = self.edi_conf_confirmed | self.edi_conf_done
        order = self.env["sale.order"].create(
            {
                "partner_id": self.partner.id,
            }
        )
        self.assertFalse(order.exchange_record_ids)
        order.with_context(fake_output="ORDER CONFIRM").action_confirm()
        self.assertEqual(len(order.exchange_record_ids), 1)
        record = order.exchange_record_ids[0]
        self.assertEqual(record._get_file_content(), "ORDER CONFIRM")
        self.assertEqual(record.type_id, self.exc_type)
        # When done, nothing changes
        order.with_context(fake_output="ORDER DONE").action_done()
        record1, record2 = order.exchange_record_ids
        self.assertEqual(record1.type_id, self.exc_type)
        self.assertEqual(record1._get_file_content(), "ORDER CONFIRM")
        self.assertEqual(record2.type_id, self.exc_type)
        self.assertEqual(record2._get_file_content(), "ORDER DONE")
