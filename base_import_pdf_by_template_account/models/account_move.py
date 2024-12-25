# Copyright 2024 Tecnativa - Víctor Martínez
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).
from base64 import b64encode

from odoo import models


class AccountMove(models.Model):
    _inherit = "account.move"

    def _import_base_import_pdf_by_template(self, file_data, new=False):
        """Method to process the PDF with base_import_pdf_by_template_account
        if any template is available (similar to account_edi_ubl_cii)."""
        template_model = self.env["base.import.pdf.template"].with_company(
            self.company_id.id
        )
        total_templates = template_model.search_count([("model", "=", self._name)])
        if total_templates == 0:
            return False
        # We need to create the attachment that we will use in the wizard because it
        # has not been created yet.
        attachment = self.env["ir.attachment"].create(
            {"name": file_data["filename"], "datas": b64encode(file_data["content"])}
        )
        self.move_type = (
            "in_invoice" if self.journal_id.type == "purchase" else "out_invoice"
        )
        # return self._import_record_base_import_pdf_by_template(invoice, attachment)
        wizard = self.env["wizard.base.import.pdf.upload"].create(
            {
                "model": self._name,
                "record_ref": f"{self._name},{self.id}",
                "attachment_ids": [(6, 0, attachment.ids)],
            }
        )
        wizard.action_process()
        return True

    def _get_edi_decoder(self, file_data, new=False):
        if file_data["type"] == "pdf":
            res = self._import_base_import_pdf_by_template(file_data, new)
            if res:
                # If everything worked correctly, we return False to avoid what
                # is done in the _extend_with_attachments() method of account
                # with the result of the _get_edi_decoder() method.
                return False
        return super()._get_edi_decoder(file_data, new=new)
