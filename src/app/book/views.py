# coding=utf-8
""" '/book' Views """
from flask import Blueprint, render_template, abort
import tools

blueprint = Blueprint('book', __name__, url_prefix="/book")


@blueprint.route('/<isbn>')
def display_book(isbn):
    """ Display a specific book based on the ISBN number
    :param isbn: isbn Number (10-digit / 13-digit)
    """

    # TODO: MongoDB Exceptions
    book = tools.get_book(isbn)
    seller_list = tools.query_sales_listing(isbn)

    if not book:
        abort(404)

    return render_template('book/book_isbn.html', book=book, seller_list=seller_list)


