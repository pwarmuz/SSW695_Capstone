#!/usr/bin/python
""" Module For Scraping Stevens Bookstore """
# Standard Library Imports
import time
import pickle
import json
import os

# 3rd Party Imports
import requests

# Project Imports
from webdrivers import get_geckodriver_path

__author__ = "Constantine Davantzis"
__status__ = "Development"


def update_book_id_list(executable_path=get_geckodriver_path()):
    """ Update stevens books id list pickle object with all books ids
    :return: Weather or not the object was updated successfully
    """
    try:
        from selenium import webdriver
    except ImportError:
        return False, "Selenium must be installed on server"

    try:
        r = []
        driver = webdriver.Firefox(executable_path=executable_path)

        def get_options_for(_id):
            select_box = driver.find_element_by_id(_id)
            return select_box.find_elements_by_tag_name("option")[1:]

        driver.get("http://www.stevenscampusstore.com/buy_textbooks.asp")
        select_term = driver.find_element_by_id("fTerm")
        select_term.find_elements_by_tag_name("option")[1].click()
        time.sleep(.5)
        for dept in get_options_for("fDept"):
            dept.click()
            time.sleep(.5)
            for course in get_options_for("fCourse"):
                course.click()
                time.sleep(.5)
                for section in get_options_for("fSection"):
                    r.append(section.get_attribute("value"))

        driver.close()
        driver.quit()

        with open('data/stevens_bookstore_ids.p', 'wb') as f:
            pickle.dump(r, f)

        return True, "data/stevens_bookstore_ids.p updated successfully"
    except Exception as e:
        return False, e.message


def get_book_id_list():
    """ Load the list of all Stevens books IDs from pickle object
    :return: List of Steevns Book Ids
    """
    try:
        return pickle.load(open('data/stevens_bookstore_ids.p', 'rb'))
    except:
        return []


def request_book_info(*ids):
    """ Make a request to stevens campus store for the books info of the ids provided """
    r = requests.post('http://www.stevenscampusstore.com/textbook_express.asp?mode=2&step=2', data={'sectionIds': ids})
    return r.content


def parse_book_info(html_doc):
    """ Parse the books info """
    from bs4 import BeautifulSoup
    d = {}
    soup = BeautifulSoup(html_doc, 'html.parser')
    # Parse Course
    for course_elm in (soup.find_all("span", {"id": "course-bookdisplay-coursename"})):
        course = course_elm.text.split(",")[0]
        d[course] = []
        table = course_elm.find_next("table", {"class": "data"})
        if table is not None:
            # Parse Course Books
            for book in table.find_all("tr", {"class": "book"}):
                _class = book.get('class')
                is_required = 'course-required' in _class
                is_optional = 'course-optional' in _class
                if is_required or is_optional:
                    book_dict = {"is_required": is_required}

                    # Parse Meta Data
                    stevens_metadata = {}
                    for x in ["book-title", "book-author", "isbn", "book-edition", "book-binding" ]:
                        book_metadata_elm = book.find("span", {"class": x})
                        if book_metadata_elm is not None:
                            stevens_metadata[x] = book_metadata_elm.text.replace(u"\u00a0", " ")

                    if stevens_metadata.get("book-title") == 'No Text Required':
                        break

                    book_dict["stevens-metadata"] = stevens_metadata

                    # Parse Book Pricing
                    stevens_pricing = {}
                    for price in book.find_all("td", {"class": "price"}):
                        price_label = price.find("label")
                        book_type = price_label.get("for")[10:].split("_")[0]
                        book_cost = price_label.text
                        if book_cost != "N/A":
                            stevens_pricing[book_type] = float(book_cost[1:])
                    book_dict["stevens-pricing"] = stevens_pricing
                    d[course].append(book_dict)
    return d


def update_book_info():
    """ Update stevens books info file """
    data = parse_book_info(request_book_info(get_book_id_list()))
    with open('data/stevens_bookstore_info.json', 'w') as f:
        json.dump(data, f, sort_keys=True, indent=4, separators=(',', ': '))


def put_stevens_book_info_into_database():
    from app import mongo_client
    dir = os.path.dirname(__file__)
    filename = os.path.join(dir, 'data\stevens_bookstore_info.json')
    with open(filename) as f:
        data = json.load(f)

    g = {}
    for k, d in data.iteritems():
        let, num = k.split(" - ")
        for book in d:
            isbn = book['stevens-metadata'].get("isbn")
            if isbn is not None:
                if isbn not in g:
                    g[isbn] = {"courses": []}
                    g[isbn]["stevens-metadata"] = book['stevens-metadata']
                    g[isbn]["stevens-pricing"] = book['stevens-pricing']
                g[isbn]["courses"].append({"letter": let, "number": num, "is_required": book["is_required"]})

    for isbn, data in g.iteritems():
        mongo_client["ssw695"]["books"].update({"_id": isbn}, data, upsert=True)


if __name__ == "__main__":
    put_stevens_book_info_into_database()
