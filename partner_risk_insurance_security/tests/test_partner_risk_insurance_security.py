from odoo.tests.common import TransactionCase


class TestPartnerRiskInsuranceSecurity(TransactionCase):
    def setUp(self):
        super().setUp()

        # Create test users
        self.full_access_user = self.env["res.users"].create(
            {
                "name": "Full Access User",
                "login": "full_access_user",
                "groups_id": [
                    (
                        6,
                        0,
                        [
                            self.env.ref(
                                "partner_risk_insurance_security."
                                "group_full_access_credit_policy_state"
                            ).id
                        ],
                    )
                ],
            }
        )

        self.regular_user = self.env["res.users"].create(
            {
                "name": "Regular User",
                "login": "regular_user",
                # No special groups assigned
            }
        )

        # Create a test partner
        self.partner = self.env["res.partner"].create(
            {"name": "Test Partner", "company_type": "company"}
        )

    def test_is_full_access_user_field(self):
        # Check with a user who has the full access group
        self.env.user = self.full_access_user  # Set the full access user
        self.assertTrue(
            self.env.user.has_group(
                "partner_risk_insurance_security.group_full_access_credit_policy_state"
            )
        )
        self.partner.invalidate_cache(["is_full_access_user"])  # Invalidate the cache
        self.assertTrue(
            self.partner.is_full_access_user,
            "User with full access group should have `is_full_access_user` set to True",
        )

        # Check with a user who doesn't have the full access group
        self.env.user = self.regular_user  # Set the regular user
        self.assertFalse(
            self.env.user.has_group(
                "partner_risk_insurance_security.group_full_access_credit_policy_state"
            )
        )
        self.partner.invalidate_cache(["is_full_access_user"])  # Invalidate the cache
        self.assertFalse(
            self.partner.is_full_access_user,
            "User without full access group should have `is_full_access_user` set to False",
        )
