# Copyright 2018 Tecnativa - Carlos Dauden
# Copyright 2018 Tecnativa - Pedro M. Baeza
# Copyright 2023 Tecnativa - Carolina Fernandez
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo import fields, models


class StockPicking(models.Model):
    _inherit = "stock.picking"

    intercompany_picking_id = fields.Many2one(comodel_name="stock.picking", copy=False)

    def action_done(self):
        for pick in self.filtered(
            lambda x: x.location_dest_id.usage == "customer"
        ).sudo():
            purchase = pick.sale_id.auto_purchase_order_id
            if not purchase:
                continue
            po_picking_pending = purchase.picking_ids.filtered(
                lambda x: x.state not in ["done", "cancel"]
            )
            po_picking_pending.intercompany_picking_id = pick.id
            if not pick.intercompany_picking_id and po_picking_pending[0]:
                pick.intercompany_picking_id = po_picking_pending[0]
            for move in pick.move_lines:
                move_lines = move.move_line_ids.filtered(lambda x: x.qty_done > 0)
                po_move_pending = move.sale_line_id.auto_purchase_line_id.move_ids.filtered(
                    lambda x, ic_pick=pick.intercompany_picking_id: x.picking_id
                    == ic_pick
                    and x.state not in ["done", "cancel"]
                )
                po_move_lines = po_move_pending.mapped("move_line_ids")
                move_line_diff = len(move_lines) - len(po_move_lines)
                # generate new move lines if needed
                # example: In purchase order of C1, we have 2 move lines
                # and in reception of C2, we have 3 move lines(with lot or serial number)
                # then we need to create 1 more move line in purchase order of C1
                if move_line_diff > 0:
                    new_move_line_vals = []
                    for _index in range(move_line_diff):
                        vals = po_move_pending._prepare_move_line_vals()
                        new_move_line_vals.append(vals)
                    po_move_lines |= po_move_lines.create(new_move_line_vals)
                # check and assign lots here
                # if len(move_lines) != (po_move_lines)
                # the zip will stop at the shortest list(only with qty_done > 0)
                # list(zip([1, 2], [1, 2, 3, 4])) = [(1, 1), (2, 2)]
                # list(zip([1, 2, 3, 4], [1, 2])) = [(1, 1), (2, 2)]
                for ml, po_ml in zip(move_lines, po_move_lines):
                    lot_id = ml.lot_id
                    if not lot_id:
                        continue
                    # search if the same lot exists in destination company
                    dest_lot = ml._get_or_create_lot_intercompany(po_ml.company_id)
                    po_ml.lot_id = dest_lot
        return super().action_done()
