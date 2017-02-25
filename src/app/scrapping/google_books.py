# coding=utf-8
""" Code to get info about a specific book using the google books api """
import requests


def get_info_by_isbn(isbn, key=None):
    """ Get book info from the google books api by isbn """
    url = "https://www.googleapis.com/books/v1/volumes?q=isbn:{}".format(isbn)

    if key is not None:
        url += "&key=" + key

    r = requests.get(url)
    if r.status_code == 200:
        j = r.json()
        if j.get("totalItems", 0) > 0:
            return j["items"][0]
    return None


def get_info_by_id(google_books_id):
    """ Get book info from the google books api by google  """
    url = "https://www.googleapis.com/books/v1/volumes/{}".format(google_books_id)
    r = requests.get(url)
    if r.status_code == 200:
        return r.json()
    return None