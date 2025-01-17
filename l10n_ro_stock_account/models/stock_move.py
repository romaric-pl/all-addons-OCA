# Copyright (C) 2014 Forest and Biomass Romania
# Copyright (C) 2020 NextERP Romania
# Copyright (C) 2020 Terrabit
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

import logging

from odoo import _, api, models
from odoo.exceptions import UserError

_logger = logging.getLogger(__name__)


class StockMove(models.Model):
    _name = "stock.move"
    _inherit = ["stock.move", "l10n.ro.mixin"]

    @api.model
    def _get_valued_types(self):
        valued_types = super()._get_valued_types()
        if self.filtered("is_l10n_ro_record"):
            valued_types += [
                "reception",  # receptie de la furnizor fara aviz
                "reception_return",  # retur la o receptie de la funizor fara aviz
                "delivery",  # livrare din stoc fara aviz
                "delivery_return",  # storno livrare
                "plus_inventory",
                "minus_inventory",
                "consumption",  # consum in productie
                "consumption_return",  # storno consum produse
                "production",  # inreg produse finite/semifabricate din productie
                "production_return",  # storno productie
                "internal_transfer",  # transfer intern
                "usage_giving",
                "usage_giving_return",
                "internal_transit_out",  # stock moves transit to internal
                "internal_transit_in",  # stock moves internal to transit
            ]
        return valued_types

    def _create_in_svl(self, forced_quantity=None):
        _logger.debug("SVL:%s" % self.env.context.get("valued_type", ""))
        svls = self.env["stock.valuation.layer"]
        l10n_ro_records = self.filtered("is_l10n_ro_record")
        if self - l10n_ro_records:
            svls = super(StockMove, self - l10n_ro_records)._create_in_svl(
                forced_quantity
            )
        if l10n_ro_records and self.env.context.get("standard"):
            svls = super(StockMove, l10n_ro_records)._create_in_svl(forced_quantity)
        return svls

    def _create_out_svl(self, forced_quantity=None):
        _logger.debug("SVL:%s" % self.env.context.get("valued_type", ""))
        svls = self.env["stock.valuation.layer"]
        l10n_ro_records = self.filtered("is_l10n_ro_record")
        if self - l10n_ro_records:
            svls = super(StockMove, self - l10n_ro_records)._create_out_svl(
                forced_quantity
            )
        if l10n_ro_records and self.env.context.get("standard"):
            svls = super(StockMove, l10n_ro_records)._create_out_svl(forced_quantity)
        return svls

    def _is_reception(self):
        """Este receptie in stoc fara aviz"""
        it_is = self.location_id.usage == "supplier" and self._is_in()
        return it_is

    def _create_reception_svl(self, forced_quantity=None):
        move = self.with_context(standard=True, valued_type="reception")
        return move._create_in_svl(forced_quantity)

    def _is_reception_return(self):
        """Este un retur la o receptie in stoc fara aviz"""
        it_is = self.location_dest_id.usage == "supplier" and self._is_out()
        return it_is

    def _create_reception_return_svl(self, forced_quantity=None):
        svl = self.env["stock.valuation.layer"]
        for move in self:
            move = move.with_context(standard=True, valued_type="reception_return")
            if (
                move.origin_returned_move_id
                and move.origin_returned_move_id.sudo().stock_valuation_layer_ids
            ):
                move = move.with_context(
                    origin_return_candidates=move.origin_returned_move_id.sudo()
                    .stock_valuation_layer_ids.filtered(lambda sv: sv.remaining_qty > 0)
                    .ids
                )
            svl += move._create_out_svl(forced_quantity)
        return svl

    def _is_delivery(self):
        """Este livrare din stoc fara aviz"""
        return self.location_dest_id.usage == "customer" and self._is_out()

    def _create_delivery_svl(self, forced_quantity=None):
        move = self.with_context(standard=True, valued_type="delivery")
        return move._create_out_svl(forced_quantity)

    def _is_delivery_return(self):
        """Este retur la o livrare din stoc fara aviz"""
        it_is = self.location_id.usage == "customer" and self._is_in()
        return it_is

    def _create_delivery_return_svl(self, forced_quantity=None):
        move = self.with_context(standard=True, valued_type="delivery_return")
        return move._create_in_svl(forced_quantity)

    def _is_plus_inventory(self):
        it_is = (
            self.location_id.usage == "inventory"
            and self.location_dest_id.usage == "internal"
        )

        return it_is

    def _create_plus_inventory_svl(self, forced_quantity=None):
        move = self.with_context(standard=True, valued_type="plus_inventory")
        return move._create_in_svl(forced_quantity)

    def _is_minus_inventory(self):
        it_is = (
            self.location_id.usage == "internal"
            and self.location_dest_id.usage == "inventory"
        )

        return it_is

    def _create_minus_inventory_svl(self, forced_quantity=None):
        move = self.with_context(standard=True, valued_type="minus_inventory")
        return move._create_out_svl(forced_quantity)

    def _is_production(self):
        """Este inregistrare intrare produse finite prin productie"""
        it_is = (
            self._is_in()
            and self.location_id.usage == "production"
            and not self.origin_returned_move_id
        )
        return it_is

    def _create_production_svl(self, forced_quantity=None):
        move = self.with_context(standard=True, valued_type="production")
        return move._create_in_svl(forced_quantity)

    def _is_production_return(self):
        """Este retur inregistrare produse finite prin productie"""
        it_is = (
            self._is_out()
            and self.location_dest_id.usage == "production"
            and self.origin_returned_move_id
        )
        return it_is

    def _create_production_return_svl(self, forced_quantity=None):
        move = self.with_context(standard=True, valued_type="production_return")
        if (
            move.origin_returned_move_id
            and move.origin_returned_move_id.sudo().stock_valuation_layer_ids
        ):
            move = move.with_context(
                origin_return_candidates=move.origin_returned_move_id.sudo()
                .stock_valuation_layer_ids.filtered(lambda sv: sv.remaining_qty > 0)
                .ids
            )

        return move._create_out_svl(forced_quantity)

    def _is_consumption(self):
        """Este un conusm de materiale in productie"""
        it_is = (
            self._is_out()
            and self.location_dest_id.usage in ("consume", "production")
            and not self.origin_returned_move_id
        )
        return it_is

    def _create_consumption_svl(self, forced_quantity=None):
        move = self.with_context(standard=True, valued_type="consumption")
        return move._create_out_svl(forced_quantity)

    def _is_consumption_return(self):
        """Este un conusm de materiale in productie"""
        it_is = (
            self._is_in()
            and self.location_id.usage in ("consume", "production")
            and self.origin_returned_move_id
        )
        return it_is

    def _create_consumption_return_svl(self, forced_quantity=None):
        move = self.with_context(standard=True, valued_type="consumption_return")
        return move._create_in_svl(forced_quantity)

    def _get_out_move_lines(self):
        "fix _get_out_move_lines return None for move to transit"
        move_lines = super()._get_out_move_lines()
        if not move_lines:
            move_lines = self.move_line_ids.filtered(
                lambda x: "transit"
                in (x.location_dest_id | x.location_id).mapped("usage")
            )
        if (
            not move_lines
            and self.env.context.get("valued_type", "") == "internal_transfer"
        ):
            move_lines = self.move_line_ids
        return move_lines

    def _get_in_move_lines(self):
        "fix _get_out_move_lines return None for move to transit"
        move_lines = super()._get_in_move_lines()

        if (
            not move_lines
            and self.env.context.get("valued_type", "") == "internal_transfer"
        ):
            move_lines = self.move_line_ids
        return move_lines

    def _is_internal_transit_in(self):
        """Este o iesire in trazit"""
        it_is = (
            self.location_dest_id.usage == "transit"
            and self.location_id.usage == "internal"
        )
        return it_is

    def _create_internal_transit_in_svl(self, forced_quantity=None):
        """
        - Se creaza SVL prin metoda _create_out_svl, dar pastram remaining
        - SVL vor fi inregistrare cu - pe contul de gestiune de origine.
        """
        svls = self.env["stock.valuation.layer"].sudo()
        # company_id = self.env.context.get("force_company", self.env.company.id)
        # company = self.env["res.company"].browse(company_id)
        # currency = company.currency_id
        moves = self.with_context(standard=True, valued_type="internal_transit_in")
        for move in moves:
            svls |= move._create_out_svl(forced_quantity)
            amount = 0
            for svl in svls:
                if svl.quantity > 0:
                    svl.write(
                        {
                            "remaining_qty": svl.quantity,
                            "remaining_value": svl.value,
                        }
                    )
                amount += svl.value / (svl.quantity or 1)
            move.price_unit = amount  #

            # vls_vals = move._prepare_common_svl_vals()
            # quantity = forced_quantity or move.quantity
            # product = move.product_id
            # vls_vals.update({
            #     'product_id': product.id,
            #     'value': currency.round(-1*quantity * product.standard_price),
            #     'unit_cost': product.standard_price,
            #     'quantity': -1*quantity,
            #     'l10n_ro_valued_type': 'internal_transit_in',
            # })
            # svls |= self.env["stock.valuation.layer"].create(vls_vals)
        return svls

    def _is_internal_transit_out(self):
        """Este o intrare din tranzit"""
        it_is = (
            self.location_dest_id.usage == "internal"
            and self.location_id.usage == "transit"
        )
        return it_is

    def _create_internal_transit_out_svl(self, forced_quantity=None):
        """
        - Se creaza SVL prin copiere, pastram remaining
        - Daca nu avem o inlantuire, si transportul este manual, iesirea de face fifo.
        - SVL vor fi inregistrare cu + pe contul de gestiune de destinatie.
        """
        svls = self.env["stock.valuation.layer"].sudo()
        # company_id = self.env.context.get("force_company", self.env.company.id)
        # company = self.env["res.company"].browse(company_id)
        # currency = company.currency_id
        moves = self.with_context(standard=True, valued_type="internal_transit_out")
        for move in moves:
            valued_move_lines = move._get_out_move_lines()
            valued_quantity = 0
            for valued_move_line in valued_move_lines:
                valued_quantity += valued_move_line.product_uom_id._compute_quantity(
                    valued_move_line.quantity, move.product_id.uom_id
                )

            svls |= move._create_in_svl(forced_quantity or valued_quantity)
            for svl in svls:
                svl.write(
                    {
                        "quantity": abs(svl.quantity),
                        "value": abs(svl.value),
                        "remaining_qty": abs(svl.quantity),
                        "remaining_value": abs(svl.value),
                    }
                )
            # vls_vals = move._prepare_common_svl_vals()
            # quantity = forced_quantity or move.quantity
            # product = move.product_id
            # vls_vals.update({
            #     'product_id': product.id,
            #     'value': currency.round(quantity * product.standard_price),
            #     'unit_cost': product.standard_price,
            #     'quantity': quantity,
            #     'l10n_ro_valued_type': 'internal_transit_out',
            # })
            # svls |= self.env["stock.valuation.layer"].create(vls_vals)
        return svls

    def _is_internal_transfer(self):
        """Este transfer intern"""
        it_is = (
            self.location_dest_id.usage == "internal"
            and self.location_id.usage == "internal"
        )
        return it_is

    # cred ca este mai bine sa generam doua svl - o intrare si o iesire
    def _create_internal_transfer_svl(self, forced_quantity=None):
        move = self.with_context(standard=True, valued_type="internal_transfer")
        svls = move._create_out_svl(forced_quantity)
        move = self.with_context(standard=True, valued_type="internal_transfer")
        svls |= move._create_in_svl(forced_quantity)
        return svls

    def _is_usage_giving(self):
        """Este dare in folosinta"""
        it_is = self.location_dest_id.usage == "usage_giving" and self._is_out()

        return it_is

    def _create_usage_giving_svl(self, forced_quantity=None):
        move = self.with_context(standard=True, valued_type="usage_giving")
        return move._create_out_svl(forced_quantity)

    def _is_usage_giving_return(self):
        """Este return dare in folosinta"""
        it_is = self.location_id.usage == "usage_giving" and self._is_in()
        return it_is

    def _create_usage_giving_return_svl(self, forced_quantity=None):
        move = self.with_context(standard=True, valued_type="usage_giving_return")
        return move._create_in_svl(forced_quantity)

    def _prepare_common_svl_vals(self):
        vals = super()._prepare_common_svl_vals()
        if self.is_l10n_ro_record:
            valued_type = self.env.context.get("valued_type")
            if valued_type:
                vals["l10n_ro_valued_type"] = valued_type
            vals[
                "l10n_ro_account_id"
            ] = self.product_id.categ_id.property_stock_valuation_account_id.id
        return vals

    def _create_dropshipped_svl(self, forced_quantity=None):
        valued_type = "dropshipped"

        svls = super(
            StockMove, self.with_context(valued_type=valued_type)
        )._create_dropshipped_svl(forced_quantity)
        for svl in svls:
            if svl.quantity < 0:
                svl.write({"l10n_ro_valued_type": "delivery"})
            if svl.quantity > 0:
                svl.write({"l10n_ro_valued_type": "reception"})
        return svls

    def _get_company(self, svl):
        self.ensure_one()
        company_from = (
            self._is_out()
            and self.mapped("move_line_ids.location_id.company_id")
            or False
        )
        company_to = (
            self._is_in()
            and self.mapped("move_line_ids.location_dest_id.company_id")
            or False
        )

        if self._is_in():
            return company_to

        if self._is_out():
            return company_from

        return self.env.company

    def _account_entry_move(self, qty, description, svl_id, cost):
        """Accounting Valuation Entries"""
        if not self.is_l10n_ro_record:
            return super()._account_entry_move(qty, description, svl_id, cost)

        svl = self.env["stock.valuation.layer"].browse(svl_id)
        company = self._get_company(svl)
        self = company and self.with_company(company.id) or self
        self = self.with_context(valued_type=svl.l10n_ro_valued_type, standard=True)

        am_vals = []
        if svl.l10n_ro_valued_type not in (
            "reception",
            "reception_return",
            "internal_transfer",
        ):
            am_vals = super()._account_entry_move(qty, description, svl_id, cost)

        if self.env.context.get("l10n_ro_reception_in_progress"):
            am_vals = super()._account_entry_move(qty, description, svl_id, cost)

        if svl.l10n_ro_valued_type == "internal_transfer":
            am_vals = self._account_entry_move_internal_transfer(
                qty, description, svl_id, cost
            )

        if svl.l10n_ro_valued_type == "internal_transit_in":
            am_vals = self._account_entry_move_internal_transit_in(
                qty, description, svl_id, cost
            )

        if svl.l10n_ro_valued_type == "internal_transit_out":
            am_vals = self._account_entry_move_internal_transit_out(
                qty, description, svl_id, cost
            )

        # todo: de eliminat
        if self.is_l10n_ro_record:
            self._l10n_ro_account_entry_move(qty, description, svl_id, cost)

        if not self.company_id.anglo_saxon_accounting and svl.l10n_ro_valued_type in [
            "delivery",
            "delivery_notice",
            "reception_notice",
        ]:
            (
                journal_id,
                acc_src,
                acc_dest,
                acc_valuation,
            ) = self._get_accounting_data_for_valuation()
            anglosaxon_am_vals = self._prepare_anglosaxon_account_move_vals(
                acc_src,
                acc_dest,
                acc_valuation,
                journal_id,
                qty,
                description,
                svl_id,
                cost,
            )
            if anglosaxon_am_vals:
                am_vals.append(anglosaxon_am_vals)

        return am_vals

    def _account_entry_move_internal_transit_in(self, qty, description, svl_id, cost):
        move = self.with_context(valued_type="internal_transit_in")
        (
            journal_id,
            acc_src,
            acc_dest,
            acc_valuation,
        ) = move._get_accounting_data_for_valuation()
        am_vals = move._prepare_account_move_vals(
            acc_src, acc_dest, journal_id, qty, description, svl_id, -1 * cost
        )
        return [am_vals]

    def _account_entry_move_internal_transit_out(self, qty, description, svl_id, cost):
        move = self.with_context(valued_type="internal_transit_out")
        (
            journal_id,
            acc_src,
            acc_dest,
            acc_valuation,
        ) = move._get_accounting_data_for_valuation()
        am_vals = move._prepare_account_move_vals(
            acc_src, acc_valuation, journal_id, qty, description, svl_id, cost
        )
        return [am_vals]

    def _account_entry_move_internal_transfer(self, qty, description, svl_id, cost):
        move = self.with_context(valued_type="internal_transfer")
        location_from = self.location_id
        location_to = self.location_dest_id
        am_vals = []
        (
            journal_id,
            acc_src,
            acc_dest,
            acc_valuation,
        ) = move._get_accounting_data_for_valuation()
        if location_to.l10n_ro_property_stock_valuation_account_id and cost < 0:
            if acc_dest != acc_valuation:
                am_vals.append(
                    move._prepare_account_move_vals(
                        acc_dest,
                        acc_valuation,
                        journal_id,
                        qty,
                        description,
                        svl_id,
                        cost,
                    )
                )
        if location_from.l10n_ro_property_stock_valuation_account_id and cost > 0:
            if acc_src != acc_valuation:
                am_vals.append(
                    move._prepare_account_move_vals(
                        acc_src,
                        acc_valuation,
                        journal_id,
                        qty,
                        description,
                        svl_id,
                        cost,
                    )
                )

        return am_vals

    def _prepare_account_move_vals(
        self,
        credit_account_id,
        debit_account_id,
        journal_id,
        qty,
        description,
        svl_id,
        cost,
    ):
        vals = super()._prepare_account_move_vals(
            credit_account_id,
            debit_account_id,
            journal_id,
            qty,
            description,
            svl_id,
            cost,
        )
        valued_type = self.env.context.get("valued_type", "indefinite")
        if "return" in valued_type and self.env.company.account_storno:
            vals["is_storno"] = True
        return vals

    def _l10n_ro_account_entry_move(self, qty, description, svl_id, cost):
        svl = self.env["stock.valuation.layer"].browse(svl_id)
        if self._is_usage_giving() or self._is_consumption():
            (
                journal_id,
                acc_src,
                acc_dest,
                acc_valuation,
            ) = self._get_accounting_data_for_valuation()
            acc_valuation_rec = self.env["account.account"].browse(acc_valuation)
            if acc_valuation_rec and acc_valuation_rec.l10n_ro_stock_consume_account_id:
                acc_valuation = acc_valuation_rec.l10n_ro_stock_consume_account_id.id
            if acc_src != acc_valuation:
                self._l10n_ro_create_account_move_line(
                    acc_valuation, acc_src, journal_id, qty, description, svl, cost
                )
        if self._is_usage_giving_return() or self._is_consumption_return():
            (
                journal_id,
                acc_src,
                acc_dest,
                acc_valuation,
            ) = self._get_accounting_data_for_valuation()
            acc_valuation_rec = self.env["account.account"].browse(acc_valuation)
            if acc_valuation_rec and acc_valuation_rec.l10n_ro_stock_consume_account_id:
                acc_valuation = acc_valuation_rec.l10n_ro_stock_consume_account_id.id
            if acc_dest != acc_valuation:
                self._l10n_ro_create_account_move_line(
                    acc_dest, acc_valuation, journal_id, qty, description, svl, cost
                )
        if self._is_usage_giving() or self._is_usage_giving_return():
            # inregistrare dare in folosinta 8035
            move = self.with_context(valued_type="usage_giving_secondary")
            (
                journal_id,
                acc_src,
                acc_dest,
                acc_valuation,
            ) = move._get_accounting_data_for_valuation()
            move._l10n_ro_create_account_move_line(
                acc_src, acc_dest, journal_id, qty, description, svl, cost
            )

    def _l10n_ro_create_account_move_line(
        self,
        credit_account_id,
        debit_account_id,
        journal_id,
        qty,
        description,
        svl_id,
        cost,
    ):
        # nu mai trebuie generate notele contabile de la cont de stoc la cont de stoc
        # valabil doar pentru dare in folosinta
        if (
            credit_account_id == debit_account_id
            and not self._is_usage_giving()
            and not self._is_usage_giving_return()
        ):
            return []
        if isinstance(svl_id, models.BaseModel):
            svl_id = svl_id.id

        account_move = self.env["account.move"].create(
            self.with_company(self.company_id)._prepare_account_move_vals(
                credit_account_id,
                debit_account_id,
                journal_id,
                qty,
                description,
                svl_id,
                cost,
            )
        )
        account_move.action_post()
        return account_move

    def _get_accounting_data_for_valuation(self):
        fiscal_pos = self.picking_id.picking_type_id.l10n_ro_fiscal_position_id
        self = self.with_context(fiscal_pos=fiscal_pos)
        (
            journal_id,
            acc_src,
            acc_dest,
            acc_valuation,
        ) = super()._get_accounting_data_for_valuation()
        if not self.is_l10n_ro_record:
            return journal_id, acc_src, acc_dest, acc_valuation

        valued_type = self.env.context.get("valued_type", "indefinite")
        location_from = self.location_id
        location_to = self.location_dest_id
        location_from_account = (
            location_from.l10n_ro_property_stock_valuation_account_id
        )
        location_to_account = location_to.l10n_ro_property_stock_valuation_account_id

        company = self.company_id
        stock_transfer_account = company.l10n_ro_property_stock_transfer_account_id

        allow_accounts_change = self.product_id.categ_id.l10n_ro_stock_account_change
        operations_not_allowed = ["usage_giving_secondary"]
        if allow_accounts_change and valued_type not in operations_not_allowed:
            # produsele din aceasta locatia folosesc pentru evaluare contul
            if location_to_account:
                # in cazul unui transfer intern se va face contare dintre
                # contul de stoc si contul din locatie
                if valued_type == "internal_transfer":
                    acc_dest = location_to_account.id
                else:
                    acc_valuation = location_to_account.id
                if valued_type == "reception":
                    acc_src = acc_valuation

            # produsele din aceasta locatia folosesc pentru evaluare contul
            if location_from_account:
                # in cazul unui transfer intern se va face contare dintre
                # contul de stoc si contul din locatie
                if valued_type == "internal_transfer":
                    acc_src = location_from_account.id
                else:
                    acc_valuation = location_from_account.id
                    acc_src = location_from_account.id
            # in cazul transferului intern se va face o singura nota
            if location_from_account and location_to_account:
                acc_valuation = location_from_account.id
            # in Romania iesirea din stoc de face de regula pe contul de cheltuiala
            if valued_type in [
                "delivery",
                "consumption",
                "usage_giving",
                "production_return",
                "minus_inventory",
                "internal_transit_in",
            ]:
                acc_dest = (
                    location_to_account.id
                    or location_from.l10n_ro_property_account_expense_location_id.id
                    or acc_dest
                )
                if location_to.usage in ["consume", "production"]:
                    acc_dest = (
                        location_to.l10n_ro_property_account_expense_location_id.id
                        or acc_dest
                    )
            elif valued_type in [
                "production",
                "delivery_return",
                "consumption_return",
                "usage_giving_return",
                "plus_inventory",
                "internal_transit_out",
            ]:
                acc_src = (
                    location_from_account.id
                    or location_to.l10n_ro_property_account_expense_location_id.id
                    or acc_src
                )

        if stock_transfer_account:
            if valued_type == "internal_transit_out":
                acc_src = stock_transfer_account.id
            elif valued_type == "internal_transit_in":
                acc_dest = stock_transfer_account.id

        if valued_type in ("consumption", "usage_giving"):
            acc_src, acc_dest, acc_valuation = self._l10n_ro_get_account_cons(
                acc_src, acc_dest, acc_valuation
            )

        if valued_type in ("consumption_return", "usage_giving_return"):
            acc_src, acc_dest, acc_valuation = self._l10n_ro_get_account_cons_return(
                acc_src, acc_dest, acc_valuation
            )

        # self.log_account(acc_src, acc_dest, acc_valuation, journal_id)

        journal_id = self._l10n_ro_get_journal_id(
            location_from, location_to, journal_id
        )
        # determina analiticul aferent jurnalului
        if journal_id:
            journal = self.env["account.journal"].browse(journal_id)
            if journal.l10n_ro_fiscal_position_id:
                fiscal_position = journal.l10n_ro_fiscal_position_id
                acc_src_rec = self.env["account.account"].browse(acc_src)
                acc_dest_rec = self.env["account.account"].browse(acc_dest)
                acc_valuation_rec = self.env["account.account"].browse(acc_valuation)

                acc_src_rec = fiscal_position.map_account(acc_src_rec)
                acc_dest_rec = fiscal_position.map_account(acc_dest_rec)
                acc_valuation_rec = fiscal_position.map_account(acc_valuation_rec)
                acc_src = acc_src_rec.id
                acc_dest = acc_dest_rec.id
                acc_valuation = acc_valuation_rec.id

        # self.log_account(acc_src, acc_dest, acc_valuation, journal_id)
        return journal_id, acc_src, acc_dest, acc_valuation

    # def log_account(self, acc_src, acc_dest, acc_valuation, journal_id):
    #     acc_dest_rec = self.env["account.account"].browse(acc_dest)
    #     acc_src_rec = self.env["account.account"].browse(acc_src)
    #     acc_valuation_rec = self.env["account.account"].browse(acc_valuation)
    #     journal_rec = self.env["account.journal"].browse(journal_id)
    #     _logger.info(
    #         "Journal: %s, AccSrc: %s, AccDest: %s, AccVal: %s",
    #         journal_rec.name,
    #         acc_src_rec.code,
    #         acc_dest_rec.code,
    #         acc_valuation_rec.code,
    #     )

    def _l10n_ro_get_account_cons(self, acc_src, acc_dest, acc_valuation):
        acc_dest_rec = self.env["account.account"].browse(acc_dest)
        if acc_dest_rec and acc_dest_rec.l10n_ro_stock_consume_account_id:
            acc_dest = acc_dest_rec.l10n_ro_stock_consume_account_id.id
        acc_valuation_rec = self.env["account.account"].browse(acc_valuation)
        if acc_valuation_rec and acc_valuation_rec.l10n_ro_stock_consume_account_id:
            acc_valuation = acc_valuation_rec.l10n_ro_stock_consume_account_id.id
        return acc_src, acc_dest, acc_valuation

    def _l10n_ro_get_account_cons_return(self, acc_src, acc_dest, acc_valuation):
        acc_src_rec = self.env["account.account"].browse(acc_src)
        if acc_src_rec and acc_src_rec.l10n_ro_stock_consume_account_id:
            acc_src = acc_src_rec.l10n_ro_stock_consume_account_id.id
        acc_valuation_rec = self.env["account.account"].browse(acc_valuation)
        if acc_valuation_rec and acc_valuation_rec.l10n_ro_stock_consume_account_id:
            acc_valuation = acc_valuation_rec.l10n_ro_stock_consume_account_id.id
        return acc_src, acc_dest, acc_valuation

    def _l10n_ro_get_journal_id(self, location_from, location_to, journal_id):
        journal_to_id = False
        journal_from_id = False
        if location_to.usage == "internal":
            journal_to_id = (
                location_to.warehouse_id.l10n_ro_property_stock_journal_id.id
            )
        if location_from.usage == "internal":
            journal_from_id = (
                location_from.warehouse_id.l10n_ro_property_stock_journal_id.id
            )

        if journal_from_id and journal_to_id and journal_from_id != journal_to_id:
            raise UserError(
                _("Transfer between locations with different journals is not allowed!")
            )
        else:
            journal_id = journal_from_id or journal_to_id or journal_id

        return journal_id

    def _l10n_ro_filter_svl_on_move_line(self, domain):
        origin_svls = self.env["stock.valuation.layer"].search(domain)
        return origin_svls

    def _get_price_unit(self):
        price_unit = super()._get_price_unit()
        if not self.is_l10n_ro_record:
            return price_unit
        if self.origin_returned_move_id:
            return price_unit
        if self.product_id.cost_method != "average":
            return price_unit

        account = (
            self.product_id.l10n_ro_property_stock_valuation_account_id
            or self.product_id.categ_id.property_stock_valuation_account_id
        )

        if self._is_out():
            if self.location_id.l10n_ro_property_stock_valuation_account_id:
                account = self.location_id.l10n_ro_property_stock_valuation_account_id
        elif self._is_in():
            # ajustarea de inventar pozitiva sa se faca la pretul din locatie
            if self.price_unit:
                return price_unit
            if self.location_dest_id.l10n_ro_property_stock_valuation_account_id:
                account = (
                    self.location_dest_id.l10n_ro_property_stock_valuation_account_id
                )
        else:
            return price_unit

        domain = [
            ("product_id", "=", self.product_id.id),
            ("l10n_ro_account_id", "=", account.id),
            ("id", "not in", self.stock_valuation_layer_ids.ids),
        ]
        valuations = self.env["stock.valuation.layer"].read_group(
            domain,
            ["value:sum", "quantity:sum"],
            ["product_id"],
        )
        for valuation in valuations:
            val = round(valuation["value"], 2)
            quantity = round(valuation["quantity"], 2)
            if quantity:
                price_unit = val / quantity
        return price_unit

    def _get_out_svl_vals(self, forced_quantity):
        svl_values = super()._get_out_svl_vals(forced_quantity)
        if self.company_id.country_id.code != "RO":
            return svl_values
        for svl_value in svl_values:
            if svl_value["quantity"] >= 0:
                continue
            stock_move_id = svl_value["stock_move_id"]
            for move in self:
                if (
                    move.id == stock_move_id
                    and move.product_id.cost_method == "average"
                ):
                    svl_value["unit_cost"] = move._get_price_unit()
                    svl_value["value"] = svl_value["quantity"] * svl_value["unit_cost"]
                    _logger.debug(svl_value)

        return svl_values
