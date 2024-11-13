# Copyright 2024 (APSL-Nagarro) - Miquel Alzanillas, Antoni Marroig
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

import requests

from odoo import _
from odoo.exceptions import UserError
from odoo.tests.common import TransactionCase


class TestBookstoreMgmtGoogleBooksApi(TransactionCase):
    @classmethod
    def setUpClass(cls):
        cls._super_send = requests.Session.send
        super().setUpClass()
        cls.book = cls.env["product.template"].create({"name": "Test", "is_book": True})

    @classmethod
    def _request_handler(cls, s, r, /, **kw):
        """Don't block external requests."""
        return cls._super_send(s, r, **kw)

    def test_action_import_from_isbn13_not_found(self):
        with self.assertRaises(UserError):
            self.book.action_import_from_isbn()
        self.book.barcode = "978849838149"
        self.assertEqual(
            self.book.action_import_from_isbn(),
            {
                "type": "ir.actions.client",
                "tag": "display_notification",
                "params": {
                    "title": _("Warning"),
                    "type": "warning",
                    "message": ("Not book found with this data"),
                    "sticky": True,
                },
            },
        )

    def test_action_import_from_isbn13(self):
        self.book.barcode = "978-8498381498"
        self.book.action_import_from_isbn()
        self.assertEqual(self.book.name, "El Principito / The Little Prince")
        self.assertEqual(self.book.author_id.name, "Antoine De Saint-exupery")
        self.assertEqual(self.book.editorial_id.name, "National Geographic Books")
        self.assertEqual(self.book.genre_id.name, "Juvenile Fiction")
        self.assertEqual(self.book.year_edition, 2016)

    def test_action_import_from_isbn10(self):
        self.book.barcode = "8498381495"
        self.book.action_import_from_isbn()
        self.assertEqual(self.book.name, "El Principito / The Little Prince")
        self.assertEqual(self.book.author_id.name, "Antoine De Saint-exupery")
        self.assertEqual(self.book.editorial_id.name, "National Geographic Books")
        self.assertEqual(self.book.genre_id.name, "Juvenile Fiction")
        self.assertEqual(self.book.year_edition, 2016)

    def test_some_record_cases(self):
        self.test_action_import_from_isbn13()
        self.book2 = self.env["product.template"].create(
            {"name": "Test2", "is_book": True}
        )
        self.env["product.book.author"].create(
            {"name": "Antoine De Saint-exupery Test"}
        )
        self.env["product.book.editorial"].create({"name": "FRIPP/EDITOR Test"})
        self.env["product.book.editorial"].create({"name": "FRIPP/EDITOR"})
        self.env["product.book.genre"].create({"name": "Fiction2"})
        self.book2.barcode = "9789874860651"
        self.book2.action_import_from_isbn()
        self.assertEqual(self.book.author_id, self.book2.author_id)
        self.assertEqual(self.book2.editorial_id.name, "FRIPP/EDITOR")
        self.assertEqual(self.book2.genre_id.name, "Juvenile Fiction")
