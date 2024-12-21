from openupgradelib import openupgrade


def _create_account_payment_method_line(env):
    # Create account payment method lines from account payment methods
    openupgrade.logged_query(
        env.cr,
        """
        INSERT INTO account_payment_method_line (name, sequence,
            payment_method_id, journal_id, create_uid, write_uid,
            create_date, write_date)
        SELECT apm.name, 10, apm.id, aj.id,
            apm.create_uid, apm.write_uid, apm.create_date, apm.write_date
        FROM account_payment_method apm, account_journal aj
        WHERE apm.code = 'sepa_credit_transfer' AND aj.type IN ('bank', 'cash')
        """,
    )


@openupgrade.migrate()
def migrate(env, version):
    _create_account_payment_method_line(env)
