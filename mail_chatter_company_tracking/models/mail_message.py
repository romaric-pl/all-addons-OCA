from odoo import models


class Message(models.Model):
    _inherit = "mail.message"

    def _message_format(self, fnames):
        vals_list = super()._message_format(fnames)
        for vals in vals_list:
            for tracking_value in vals["tracking_value_ids"]:
                tracking = self.env["mail.tracking.value"].browse(tracking_value["id"])
                tracking_value.update(
                    {
                        "company_name": (
                            tracking.company_id.name
                            if self.env[tracking.field.model]
                            ._fields[tracking.field.name]
                            .company_dependent
                            else False
                        ),
                    }
                )
        return vals_list
