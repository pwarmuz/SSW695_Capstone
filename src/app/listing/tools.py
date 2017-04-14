from app import mongo_client


def get_ten_list():
    """ Get books listed top10
        Temp, redundant
        Demonstrates example, should be replaced with finding a count of top listed books
    :return:
    """

    return mongo_client.ssw695.books.find().limit(10)




