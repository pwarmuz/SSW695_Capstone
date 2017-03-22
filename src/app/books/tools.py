""" '/books' tools """
from app import mongo_client


def get_book(isbn):
    """ Get book by isbn
    :return:
    """
    if len(isbn) == 13:
        return mongo_client.ssw695.books.find_one({"google-metadata.volumeInfo.industryIdentifiers.1.identifier": isbn})

    return mongo_client.ssw695.books.find_one({"_id": isbn})


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
        validate_isbn10(isbn)
    except ValueError:
        return False
    return True


def is_isbn(isbn):
    return True if is_isbn10(isbn) or is_isbn13(isbn) else False


def isbn10_checksum(isbn):
    r = 11 - sum(int(isbn[i]) * (10 - i) for i in xrange(9)) % 11
    return str(r) if r < 10 else "X"


def isbn13_checksum(isbn):
    x = map(int, list(isbn))
    r = 10 - sum(
        [x[0], 3 * x[1], x[2], 3 * x[3], x[4], 3 * x[5], x[6], 3 * x[7], x[8], 3 * x[9], x[10], 3 * x[11]]) % 10
    return str(r) if r < 10 else "0"


def isbn10_to_isbn13(isbn):
    # Add 978 prefix and remove isbn10 checksum digit
    isbn = "978" + isbn[:-1]
    return isbn + isbn13_checksum(isbn)


def isbn13_to_isbn10(isbn):
    # Remove 978 prefix and remove isbn13 checksum digit
    if not isbn.beginswith("978"):
        raise ValueError("Only ISBNs with prefix of 978 can be converted")
    isbn = isbn[3:-1]
    return isbn + isbn10_checksum(isbn)

