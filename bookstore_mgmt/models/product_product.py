# Copyright 2024 (APSL-Nagarro) - Miquel Alzanillas, Antoni Marroig
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo import fields, models


class ProductProduct(models.Model):
    _inherit = "product.product"

    is_book = fields.Boolean(string="Is a book")
    author_id = fields.Many2one("product.book.author", string="Author")
    editorial_id = fields.Many2one("product.book.editorial", string="Editorial")
    genre_id = fields.Many2one("product.book.genre", string="Genre")
    year_edition = fields.Integer(string="Year of Edition")
