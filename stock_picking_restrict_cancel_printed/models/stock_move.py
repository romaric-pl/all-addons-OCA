# Copyright 2024 Jacques-Etienne Baudoux (BCIM) <je@bcim.be>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from odoo import _, models
from odoo.exceptions import UserError


class StockMove(models.Model):
    _inherit = "stock.move"

    def _action_cancel(self):
        # if picking_type create_backorder is never, then move is canceled on action_done
        if self.env.context.get("cancel_backorder"):
            return super()._action_cancel()
        for move in self:
            if (
                move.picking_id.printed
                and move.picking_type_id.restrict_cancel_if_printed
            ):
                raise UserError(
                    _("You cannot cancel a transfer that is already printed.")
                )
        return super()._action_cancel()
