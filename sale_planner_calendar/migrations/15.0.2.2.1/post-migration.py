# Copyright 2024 Tecnativa - Carlos Dauden
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
from openupgradelib import openupgrade


def _remove_renamed_selection_values(env):
    """After rename value from upper to lower the values are duplicated.
    This method removes old upper values"""
    week_list_field = env.ref(
        "sale_planner_calendar.field_sale_planner_calendar_wizard__week_list"
    )
    value_ids = week_list_field.selection_ids.filtered(lambda x: x.value.isupper()).ids
    if value_ids:
        openupgrade.logged_query(
            env.cr,
            """
            DELETE FROM ir_model_fields_selection
            WHERE id in %(selection_value_ids)s
            """,
            {"selection_value_ids": tuple(value_ids)},
        )


@openupgrade.migrate()
def migrate(env, version):
    _remove_renamed_selection_values(env)
