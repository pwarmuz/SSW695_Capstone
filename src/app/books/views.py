# coding=utf-8
""" '/books' Views """
from flask import Blueprint, render_template, abort, session
import tools

blueprint = Blueprint('books', __name__, url_prefix="/books")


@blueprint.route('/')
def display_all_books():
    """ Display All Books """
    return render_template('books/all.html', books=list(tools.get_all_books()))


@blueprint.route('/<isbn>')
def display_book(isbn):
    """ Display a specific books based on the ISBN number
    :param isbn: isbn Number (10-digit / 13-digit)
    """

    # TODO: MongoDB Exceptions
    book = tools.get_book(isbn)

    if not book:
        abort(404)

    seller_list = tools.query_sales_listing(isbn)

    amazon_listing = None

    try:
        amazon_listing = tools.get_amazon_price(isbn)
    except:
        print "error interfacing with the amazon api"

    session['isbn_value'] = isbn
    return render_template('books/book_isbn.html', book=book, seller_list=seller_list, amazon_listing=amazon_listing)




