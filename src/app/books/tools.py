""" '/books' tools """
from app import mongo_client


def get_books(number):
    """ Get books
    :return:
    """
    return mongo_client.ssw695.books.find({"_id": number})
