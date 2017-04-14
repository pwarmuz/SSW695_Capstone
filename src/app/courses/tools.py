""" Courtses tools """
from app import mongo_client
import re
import pymongo

from constants import DEPARTMENTS


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


def get_course(letter, number):
    """ Get courses
    :return:
    """
    return mongo_client.catalog.courses.find_one_and_update({"letter": letter.upper(), "number": number},
                                                            {'$inc': {'query_score': 1}})


def get_top_courses(count=10):
    return mongo_client.catalog.courses.find().sort("query_score", pymongo.DESCENDING).limit(count)


def get_books_by_course(letter, number):
    """ Get books by course
    :return:
    """
    return mongo_client.ssw695.books.find({"courses.letter": letter.upper(), "courses.number": number})


def search_courses(input):
    """ Search courses 
    :return: A list of courses matching the input
    """
    m = re.match(r"(\w{1,3})[-]*(\d{3})", input)
    if m:
        result = get_course(m.group(1), m.group(2))
        if result:
            return [result]

    ensure_search_index()
    return list(mongo_client.catalog.courses.find({"$text": {"$search": str(input)}}))


def ensure_search_index():
    from pymongo import TEXT
    mongo_client.catalog.courses.ensure_index([('name', TEXT),
                                               ('letter', TEXT),
                                               ('number', TEXT)],
                                              default_language='english',
                                              name="search_index")
