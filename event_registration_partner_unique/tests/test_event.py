# Copyright 2016 Antiun Ingeniería S.L. - Jairo Llopis
# Copyright 2020 Tecnativa - Víctor Martínez
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from odoo import fields
from odoo.exceptions import ValidationError
from odoo.tests.common import TransactionCase


class DuplicatedPartnerCase(TransactionCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        # Remove this variable in v16 and put instead:
        # from odoo.addons.base.tests.common import DISABLED_MAIL_CONTEXT
        DISABLED_MAIL_CONTEXT = {
            "tracking_disable": True,
            "mail_create_nolog": True,
            "mail_create_nosubscribe": True,
            "mail_notrack": True,
            "no_reset_password": True,
        }
        cls.env = cls.env(context=dict(cls.env.context, **DISABLED_MAIL_CONTEXT))
        cls.event = cls.env["event.event"].create(
            {
                "name": "Test event",
                "date_begin": fields.Datetime.now(),
                "date_end": fields.Datetime.now(),
            }
        )
        cls.event.forbid_duplicates = False
        cls.partner = cls.env["res.partner"].create({"name": "Mr. Odoo"})
        cls.registration = cls.env["event.registration"].create(
            {
                "event_id": cls.event.id,
                "partner_id": cls.partner.id,
                "attendee_partner_id": cls.partner.id,
            }
        )

    def test_allowed(self):
        """No problem when it is not forbidden."""
        self.registration.copy()

    def test_forbidden(self):
        """Cannot when it is forbidden."""
        self.event.forbid_duplicates = True
        with self.assertRaises(ValidationError):
            self.registration.copy(
                {"attendee_partner_id": self.registration.attendee_partner_id.id}
            )

    def test_saved_in_exception(self):
        """The failing partners are saved in the exception."""
        self.event.forbid_duplicates = True
        with self.assertRaisesRegex(
            ValidationError, "Duplicated partners found in event"
        ):
            self.registration.copy(
                {"attendee_partner_id": self.registration.attendee_partner_id.id}
            )

    def test_duplicates_already_exist(self):
        """Cannot forbid what already happened."""
        self.registration.copy(
            {"attendee_partner_id": self.registration.attendee_partner_id.id}
        )
        with self.assertRaises(ValidationError):
            self.event.forbid_duplicates = True
