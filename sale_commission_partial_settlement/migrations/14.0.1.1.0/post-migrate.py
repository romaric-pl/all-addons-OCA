from openupgradelib import openupgrade


def unlink_orphan_agent_partials(env):
    """
    Delete agent partials that are not linked
    to a settlement line
    e.g. because the settlement was deleted
    but the ailap was left behind
    """
    openupgrade.logged_query(
        env.cr,
        """
        SELECT id
        FROM account_invoice_line_agent_partial
        WHERE id not in
            (SELECT agent_line_partial_id
            FROM settlement_agent_line_partial_rel)
        """,
    )
    ids = [row[0] for row in env.cr.fetchall()]
    env["account.invoice.line.agent.partial"].browse(ids).unlink()


def recompute_partial_settled(env):
    """
    "partial_settled" was not recomputed properly if a
    settlement was canceled or deleted
    """
    env["account.invoice.line.agent"].search(
        [
            ("commission_id.payment_amount_type", "=", "paid"),
            ("partial_settled", "!=", 0),
        ]
    )._compute_partial_settled()


def recompute_settled(env):
    """
    Sometimes AILA were not marked as "settled" properly
    for commissions of type "paid"
    """
    env["account.invoice.line.agent"].search(
        [
            ("commission_id.payment_amount_type", "=", "paid"),
        ]
    )._compute_settled()


@openupgrade.migrate()
def migrate(env, version):
    unlink_orphan_agent_partials(env)
    recompute_partial_settled(env)
    recompute_settled(env)
