""" '/books' tools """
from app import mongo_client


def get_book(isbn):
    """ Get book by isbn
    :return:
    """
    if len(isbn) == 13:
        return mongo_client.ssw695.books.find_one({"google-metadata.volumeInfo.industryIdentifiers.1.identifier": isbn})

    return mongo_client.ssw695.books.find_one({"_id": isbn})
