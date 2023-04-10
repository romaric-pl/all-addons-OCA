# Copyright 2018-2021 Akretion France (http://www.akretion.com/)
# @author: Alexis de Lattre <alexis.delattre@akretion.com>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

import logging

from odoo import _, api, fields, models
from odoo.exceptions import UserError

logger = logging.getLogger(__name__)


class AccountInvoiceChorusSend(models.TransientModel):
    _name = "account.invoice.chorus.send"
    _description = "Send several invoices to Chorus"

    @api.model
    def default_get(self, fields_list):
        res = super().default_get(fields_list)
        assert (
            self._context.get("active_model") == "account.move"
        ), "Wrong active_model, should be account.move"
        assert self._context.get("active_ids"), "Missing active_ids in ctx"
        invoices = self.env["account.move"].browse(self._context.get("active_ids"))
        company = False
        for invoice in invoices:
            if invoice.move_type not in ("out_invoice", "out_refund"):
                raise UserError(
                    _(
                        "Move '%s' is not a customer invoice. You can only send "
                        "customer invoices/refunds to Chorus."
                    )
                    % invoice.display_name
                )
            if invoice.state != "posted":
                raise UserError(
                    _(
                        "The state of invoice '{invoice_display_name}' is "
                        "'{invoice_state}'. You can only send to Chorus invoices "
                        "in posted state."
                    ).format(
                        invoice_display_name=invoice.display_name,
                        invoice_state=invoice._fields["state"].convert_to_export(
                            invoice.state, invoice
                        ),
                    )
                )
            if invoice.transmit_method_code != "fr-chorus":
                raise UserError(
                    _(
                        "On invoice '{invoice_display_name}', the transmit method is "
                        "'{transmit_method_name}'. To be able "
                        "to send it to Chorus, the transmit method must be "
                        "'Chorus'."
                    ).format(
                        invoice_display_name=invoice.display_name,
                        transmit_method_name=invoice.transmit_method_id.name
                        or _("None"),
                    )
                )
            if invoice.chorus_flow_id:
                raise UserError(
                    _(
                        "The invoice '{invoice_display_name}' has already been sent: "
                        "it is linked to Chorus Flow {flow}."
                    ).format(
                        invoice_display_name=invoice.display_name,
                        flow=invoice.chorus_flow_id.display_name,
                    )
                )
            if company:
                if company != invoice.company_id:
                    raise UserError(
                        _("All the selected invoices must be in the same company")
                    )
            else:
                company = invoice.company_id
                company._check_chorus_invoice_format()

        res.update(
            {
                "invoice_ids": [(6, 0, invoices.ids)],
                "invoice_count": len(invoices),
                "company_id": company.id,
            }
        )
        return res

    invoice_ids = fields.Many2many(
        "account.move", string="Invoices to Send", readonly=True
    )
    invoice_count = fields.Integer(string="Number of Invoices", readonly=True)
    company_id = fields.Many2one("res.company", string="Company", readonly=True)
    chorus_invoice_format = fields.Selection(
        related="company_id.fr_chorus_invoice_format", readonly=True
    )

    def run(self):
        logger.info("Starting to send invoices IDs %s to Chorus", self.invoice_ids.ids)
        company = self.company_id
        api_params = company.chorus_get_api_params(raise_if_ko=True)
        url_path = "factures/v1/deposer/flux"
        payload = self.invoice_ids.prepare_chorus_deposer_flux_payload()
        attach = self.env["ir.attachment"].create(
            {
                "name": payload.get("nomFichier"),
                "datas": payload.get("fichierFlux"),
            }
        )
        logger.info(
            "Start to send invoice IDs %s via Chorus %sWS",
            self.invoice_ids.ids,
            api_params["qualif"] and "QUALIF. " or "",
        )
        answer, session = company.chorus_post(api_params, url_path, payload)
        if answer and answer.get("numeroFluxDepot"):
            flow = self.env["chorus.flow"].create(
                {
                    "name": answer["numeroFluxDepot"],
                    "date": answer.get("dateDepot"),
                    "syntax": company.fr_chorus_invoice_format,
                    "attachment_id": attach.id,
                    "company_id": company.id,
                    "initial_invoice_ids": self.invoice_ids.ids,
                }
            )
            self.invoice_ids.write(
                {
                    "chorus_flow_id": flow.id,
                    "is_move_sent": True,
                }
            )
            action = (
                self.env.ref("l10n_fr_chorus_account.chorus_flow_action")
                .sudo()
                .read()[0]
            )
            action.update(
                {
                    "view_mode": "form,tree",
                    "views": False,
                    "res_id": flow.id,
                }
            )
            return action
        return
