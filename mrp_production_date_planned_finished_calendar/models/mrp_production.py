# Copyright 2024 ForgeFlow S.L. (https://www.forgeflow.com)
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo import models


class MrpProduction(models.Model):
    _inherit = "mrp.production"

    def _get_date_planned_start_using_delays(self):
        warehouse = self.picking_type_id.warehouse_id
        date_planned_start = self.date_planned_finished
        if warehouse.calendar_id:
            delay = self.product_id.produce_delay + self.company_id.manufacturing_lead
            return warehouse.calendar_id.plan_days(-1 * (delay + 1), date_planned_start)
        return super()._get_date_planned_start_using_delays()
