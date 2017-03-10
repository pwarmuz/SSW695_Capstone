""" '/books' tools """
from app import mongo_client

'''
def get_courses_by_departments():
    """ Get courses by departments
    :return:
    """
    cursor = mongo_client.catalog.courses.aggregate([{"$sort": {"number": 1}},
                                                     {"$group": {"_id": "$letter",
                                                                 "nodes": {"$push": {
                                                                     "a_attr": {"data-letter": "$letter",
                                                                                "data-number": "$number"},
                                                                     "text": {"$concat": ["$letter", "-",
                                                                                          "$number", " ",
                                                                                          "$name"]}}}}},
                                                     {"$sort": {"_id": 1}},
                                                     {"$project": {"_id": 0, "text": "$_id", "children": "$nodes"}}])
    for node in cursor:
        node["text"] = "{0}: {1}".format(node["text"], DEPARTMENTS.get(node["text"], ""))
        yield node
'''


def get_books(number):
    """ Get books
    :return:
    """
    return mongo_client.ssw695.books.find({"_id": number})
