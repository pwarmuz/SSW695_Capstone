""" '/books' tools """
from app import mongo_client


def get_book(isbn):
    """ Get books
    :return:
    """
    return mongo_client.ssw695.books.find_one({"_id": isbn})
