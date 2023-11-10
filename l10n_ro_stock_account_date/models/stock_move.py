# Copyright (C) 2022 NextERP Romania SRL
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from datetime import date, timedelta

from dateutil.relativedelta import relativedelta

from odoo import _, fields, models
from odoo.exceptions import UserError


class StockMove(models.Model):
    _name = "stock.move"
    _inherit = ["stock.move", "l10n.ro.mixin"]

    def l10n_ro_get_move_date(self):
        self.ensure_one()
        new_date = self._context.get("force_period_date")
        if not new_date:
            if self.picking_id:
                if self.picking_id.l10n_ro_accounting_date:
                    new_date = self.picking_id.l10n_ro_accounting_date
            elif self.inventory_id:
                new_date = self.inventory_id.accounting_date
            elif "raw_material_production_id" in self._fields:
                if self.raw_material_production_id:
                    new_date = self.raw_material_production_id.date_planned_start
                elif self.production_id:
                    new_date = self.production_id.date_planned_start
            if not new_date:
                new_date = fields.datetime.now()
        return new_date

    def _action_done(self, cancel_backorder=False):
        moves_todo = super()._action_done(cancel_backorder=cancel_backorder)
        for move in moves_todo.filtered("is_l10n_ro_record"):
            move.date = move.l10n_ro_get_move_date()
            restrict_date = move.company_id.l10n_ro_restrict_stock_move_date_last_month
            restrict_date_future = (
                move.company_id.l10n_ro_restrict_stock_move_date_future
            )

            if restrict_date:
                # se verifica daca data este in intervalul permis
                last_day_of_prev_month = date.today().replace(day=1) - timedelta(days=1)
                start_day_of_prev_month = date.today().replace(day=1) - timedelta(
                    days=last_day_of_prev_month.day
                )
                if restrict_date_future:
                    end_day_of_current_month = date.today()
                else:
                    end_day_of_current_month = (
                        date.today().replace(day=1)
                        + relativedelta(months=1)
                        - relativedelta(days=1)
                    )

                if not (
                    start_day_of_prev_month
                    <= move.date.date()
                    <= end_day_of_current_month
                ):
                    raise UserError(
                        _("Cannot validate stock move due to date restriction.")
                    )
                move.check_lock_date(move.date)

        return moves_todo

    def _trigger_assign(self):
        res = super()._trigger_assign()
        for move in self.filtered("is_l10n_ro_record"):
            move.date = move.l10n_ro_get_move_date()
        return res

    def _get_price_unit(self):
        # Update price unit for purchases in different currencies with the
        # reception date.
        if self.is_l10n_ro_record:
            if (
                self.origin_returned_move_id
                and self.origin_returned_move_id.sudo().stock_valuation_layer_ids
            ):
                # in acest caz trebuie sa se execute din l10n_ro_stock_account
                return super()._get_price_unit()

            if self.picking_id.date and self.purchase_line_id:
                po_line = self.purchase_line_id
                order = po_line.order_id
                price_unit = po_line.price_unit
                if po_line.product_qty != 0.0:
                    price_unit = po_line.price_subtotal / po_line.product_qty

                if po_line.taxes_id:
                    price_unit = po_line.taxes_id.with_context(round=False).compute_all(
                        price_unit,
                        currency=order.currency_id,
                        quantity=1.0,
                        product=po_line.product_id,
                        partner=order.partner_id,
                    )["total_excluded"]
                if po_line.product_uom.id != po_line.product_id.uom_id.id:
                    price_unit *= (
                        po_line.product_uom.factor / po_line.product_id.uom_id.factor
                    )
                if order.currency_id != order.company_id.currency_id:
                    price_unit = order.currency_id._convert(
                        price_unit,
                        order.company_id.currency_id,
                        self.company_id,
                        self.picking_id.l10n_ro_accounting_date
                        or fields.datetime.now(),
                        round=False,
                    )
                self.write(
                    {
                        "price_unit": price_unit,
                        "date": self.picking_id.l10n_ro_accounting_date
                        or fields.datetime.now(),
                    }
                )
                return price_unit
        return super()._get_price_unit()

    def _account_entry_move(self, qty, description, svl_id, cost):
        self.ensure_one()
        if self.is_l10n_ro_record:
            val_date = self.l10n_ro_get_move_date()
            self = self.with_context(force_period_date=val_date)
        return super(StockMove, self)._account_entry_move(
            qty, description, svl_id, cost
        )

    def check_lock_date(self, move_date):
        lock_date = self.env.user.company_id._get_user_fiscal_lock_date()
        if move_date.date() < lock_date:
            raise UserError(
                _("Cannot validate stock move due to account date restriction.")
            )
