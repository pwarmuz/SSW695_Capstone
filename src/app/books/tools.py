""" '/books' tools """
from app import mongo_client


def get_book(isbn):
    """ Get book by isbn
    :return:
    """
    return mongo_client.ssw695.books.find_one({"_id": isbn})
