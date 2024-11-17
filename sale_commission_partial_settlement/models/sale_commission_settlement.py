from odoo import models


class Settlement(models.Model):
    _inherit = "sale.commission.settlement"

    def unlink(self):
        self.mapped("line_ids.agent_line_partial_ids").unlink()
        return super().unlink()
