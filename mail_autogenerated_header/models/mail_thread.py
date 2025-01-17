# Copyright 2018 Therp BV <https://therp.nl>
# Copyright 2022 Hunki Enterprises BV <https://hunki-enterprises.com>
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
import logging

from odoo import api, models

_logger = logging.getLogger(__name__)


class MailThread(models.AbstractModel):
    _inherit = "mail.thread"

    @api.model
    def _message_route_process(self, message, message_dict, routes):
        # Set context key to suppress notification for autogenerated incoming mails
        if self._message_route_process_autoreply(message, message_dict, routes):
            _logger.info(
                "Ignoring email %s from %s because it seems to be an auto " "reply",
                message.get("Message-ID"),
                message.get("From"),
            )
            self = self.with_context(mail_autogenerated_header=message)
        return super()._message_route_process(
            message,
            message_dict,
            routes,
        )

    def _notify_thread(self, message, msg_vals=False, **kwargs):
        # Inhibit notifications if this is the notification for an incoming
        # autogenerated mail from another system
        if self.env.context.get("mail_autogenerated_header"):
            return False
        return super()._notify_thread(message, msg_vals=msg_vals, **kwargs)

    @api.model
    def _message_route_process_autoreply(self, message, message_dict, routes):
        """Determine if some message is an autoreply"""
        return (
            message["Auto-Submitted"]
            and message["Auto-Submitted"] != "no"
            or message["X-Auto-Response-Suppress"]
            and set(message["X-Auto-Response-Suppress"].split(", "))
            & set(["AutoReply", "All"])
        )
