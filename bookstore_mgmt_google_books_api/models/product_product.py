# Copyright 2024 (APSL-Nagarro) - Miquel Alzanillas, Antoni Marroig
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from datetime import datetime

from google_books_api_wrapper.api import GoogleBooksAPI

from odoo import _, models
from odoo.exceptions import UserError


class Product(models.Model):
    _inherit = "product.product"

    def action_import_from_isbn(self):
        for record in self.filtered(lambda x: x.is_book):
            if record.barcode:
                client = GoogleBooksAPI()
                isbn = record.barcode.replace("-", "")
                book = client.get_book_by_isbn13(isbn)
                if not book:
                    book = client.get_book_by_isbn10(isbn)
                if book:
                    # Set data to be updated
                    data = {
                        "name": book.title,
                    }

                    if book.published_date:
                        # Convert to year format
                        try:
                            published_year = datetime.strptime(
                                book.published_date, "%Y-%m-%d"
                            ).year
                        except Exception:
                            published_year = book.published_date

                        data["year_edition"] = published_year

                    if book.authors:
                        data["author_id"] = record.get_author_id(book.authors[0])

                    if book.publisher:
                        data["editorial_id"] = record.get_editorial_id(book.publisher)

                    if book.subjects:
                        data["genre_id"] = record.get_genre_id(book.subjects)

                    if book.description:
                        data["description"] = book.description
                        data["description_sale"] = book.description

                    if book.large_thumbnail:
                        data["image_1920"] = record.get_convert_to_base64(
                            book.large_thumbnail
                        )

                    # Update book data in Odoo
                    record.write(data)

                    # Show success notification
                    self.env.user.notify_success(
                        message=_("Book data updated from Google Books API")
                    )

                else:
                    # Return not found notification
                    return {
                        "type": "ir.actions.client",
                        "tag": "display_notification",
                        "params": {
                            "title": _("Warning"),
                            "type": "warning",
                            "message": _("Not book found with this data"),
                            "sticky": True,
                        },
                    }
            else:
                raise UserError(_("ISBN code is mandatory. Please, provide one."))
