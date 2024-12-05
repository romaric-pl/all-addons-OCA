# Copyright 2024 Camptocamp SA
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo.addons.component.core import Component


class EDIConfigSOListener(Component):
    _name = "edi.listener.config.sale.order"
    _inherit = "base.event.listener"
    _apply_on = ["sale.order"]

    def on_record_create(self, record, fields=None):
        trigger = "on_record_create"
        return self._exec_conf(record, trigger)

    def on_record_write(self, record, fields=None):
        trigger = "on_record_write"
        return self._exec_conf(record, trigger)

    def on_edi_sale_order_state_change(self, record, state=None):
        trigger = "on_edi_sale_order_state_change"
        return self._exec_conf(record, trigger)

    def _exec_conf(self, record, trigger, conf_field="edi_sale_conf_ids"):
        confs = record.partner_id[conf_field].edi_get_conf(trigger)
        for conf in confs:
            conf.edi_exec_snippet_do(record)
