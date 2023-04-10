# Copyright 2017 Sergio Teruel <sergio.teruel@tecnativa.com>
# Copyright 2019 David Vidal <david.vidal@tecnativa.com>
# Copyright 2021 Moka Tourisme (https://www.mokatourisme.fr).
# @author Iván Todorovich <ivan.todorovich@gmail.com>
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

from odoo import fields, models


class SaleReport(models.Model):
    _inherit = "sale.report"

    # TODO: event_id and event_ticket_id should be proposed in odoo core
    event_id = fields.Many2one(
        comodel_name="event.event",
        string="Event",
        readonly=True,
    )
    event_ticket_id = fields.Many2one(
        comodel_name="event.event.ticket",
        string="Event Ticket",
        readonly=True,
    )
    event_session_id = fields.Many2one(
        comodel_name="event.session",
        string="Event Session",
        readonly=True,
    )

    def _query(self, with_clause="", fields=None, groupby="", from_clause=""):
        fields = fields or {}
        fields["event_id"] = ", l.event_id as event_id"
        fields["event_ticket_id"] = ", l.event_ticket_id as event_ticket_id"
        fields["event_session_id"] = ", l.event_session_id as event_session_id"
        groupby += ", l.event_id, l.event_ticket_id, l.event_session_id"
        return super()._query(with_clause, fields, groupby, from_clause)
