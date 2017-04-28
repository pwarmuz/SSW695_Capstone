""" '/book' tools """
from app import mongo_client
import pymongo
from amazonproduct import API as AWS_API
"""
    ISBN algorithms https://en.wikipedia.org/wiki/International_Standard_Book_Number
"""


def get_all_books():
    """ Get All Books
    :return:
    """
    return mongo_client.ssw695.books.aggregate([{"$project": {"_id": 0, "isbn10": "$_id", "title": {
        "$ifNull": ["$google-metadata.volumeInfo.title", "$stevens-metadata.book-title"]}}},
                                                {"$sort": {"title": 1}}])


def get_book(isbn):
    """ Get books by isbn
    :return: books item from db
    """
    if is_isbn13(isbn) and isbn.startswith("978"):
        isbn = isbn13_to_isbn10(isbn)

    if is_isbn10(isbn):
        return mongo_client.ssw695.books.find_one_and_update({"_id": isbn},
                                                             {'$inc': {'query_score': 1}})


def get_top_books(count=10):
    return mongo_client.ssw695.books.find().sort("query_score", pymongo.DESCENDING).limit(count)


def validate_by_isbn(isbn):
    """ Validates the ISBN
    :param isbn: isbn Number (10-digit / 13-digit)
    """

    if is_isbn(isbn):
        book = get_book(isbn)
        if book:
            return True

    return False


def validate_isbn10(isbn):
    if len(isbn) != 10:
        raise ValueError("ISBN10 has invalid length")
    if isbn10_checksum(isbn[:-1]) != isbn[-1]:
        raise ValueError("ISBN10 has invalid checksum")


def validate_isbn13(isbn):
    if len(isbn) != 13:
        raise ValueError("ISBN13 has invalid length")
    if isbn13_checksum(isbn[:-1]) != isbn[-1]:
        raise ValueError("ISBN13 has invalid checksum")


def is_isbn10(isbn):
    try:
        validate_isbn10(isbn)
    except ValueError:
        return False
    return True


def is_isbn13(isbn):
    try:
        validate_isbn13(isbn)
    except ValueError:
        return False
    return True


def is_isbn(isbn):
    return True if is_isbn10(isbn) or is_isbn13(isbn) else False


def isbn10_checksum(isbn):
    """
    :return: the last checksum digit
    """
    r = (11 - (sum(int(isbn[i]) * (10 - i) for i in xrange(0, 9)) % 11)) % 11
    return str(r) if r < 10 else "X"


def isbn13_checksum(isbn):
    """
    :return: the last checksum digit
    """
    x = map(int, list(isbn))
    r = 10 - sum(
        [x[0], 3 * x[1], x[2], 3 * x[3], x[4], 3 * x[5], x[6], 3 * x[7], x[8], 3 * x[9], x[10], 3 * x[11]]
    ) % 10
    return str(r) if r < 10 else "0"


def isbn10_to_isbn13(isbn):
    # Add 978 prefix and remove isbn10 checksum digit
    isbn = "978" + isbn[:-1]
    return isbn + isbn13_checksum(isbn)


def isbn13_to_isbn10(isbn):
    # Remove 978 prefix and remove isbn13 checksum digit
    if not isbn.startswith("978"):
        raise ValueError("Only ISBNs with prefix of 978 can be converted")
    isbn = isbn[3:-1]
    return isbn + isbn10_checksum(isbn)


def search_titles(input):
    """ Searches all books titles
    :param: input - the title to search for
    :return: list of books matching the search
    """
    return list(mongo_client.ssw695.books.find({"$text": {"$search": str(input)}}))


def query_sales_listing(isbn):
    """ Query the sales listing from the ISBN Sales page
    :param: isbn - the isbn to search for
    :return: list of sales transactions matching the search
    """
    return list(mongo_client.ssw695.listing.find({"isbn": str(isbn), "transaction": "listed"}))


def get_amazon_price(isbn):
    """ Query amazon for the current listed price
    :param isbn - the isbn to search for 
    :return dict with url and prices
    """

    api = AWS_API(locale='us')

    result = api.item_lookup(isbn, SearchIndex='All', IdType='ISBN', ResponseGroup='Offers')
    if not len (result):
        return None

    r = {}
    r['url'] = result.Items.Item.Offers.MoreOffersUrl

    prices = []
    for offer in result.Items.Item.Offers.Offer:
        prices.append('%s %s' % (offer.OfferListing.Price.FormattedPrice, offer.OfferListing.Price.CurrencyCode))

    r['prices'] = prices

    return r


def isbn_to_title(isbn):
    """ Convert ISBN to Stevens Book Title """
    book = get_book(isbn)
    if book is not None:
        title = book.get("stevens-metadata", {}).get("book-title")
        if title is not None:
            return title
    return "No Title Found"
