# Copyright 2024 Dixmit
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

from odoo.addons.mail.controllers.discuss import DiscussController


class GatewayDiscussController(DiscussController):
    def _get_allowed_message_post_params(self):
        result = super()._get_allowed_message_post_params()
        result.add("gateway_notifications")
        return result
