#!/usr/bin/python
# coding=utf-8
""" Module For Scraping Stevens Bookstore """
import time
import pickle
import requests
import json

from selenium import webdriver

from webdrivers import get_geckodriver_path

__author__ = "Constantine Davantzis"
__status__ = "Development"


def update_book_id_list(executable_path=get_geckodriver_path()):
    """

    :return:
    """
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

    with open('book_id_list.p', 'wb') as f:
        pickle.dump(r, f)

    return True, "book_id_list.p updated successfully"


def get_book_id_list():
    return pickle.load(open('book_id_list.p', 'rb'))


def save_all_books_page():
    r = requests.post('http://www.stevenscampusstore.com/textbook_express.asp?mode=2&step=2', data={'sectionIds': get_book_id_list()})
    with open("all_books.html", "w") as text_file:
        text_file.write(r.content)


def parse_all_books_page():
    from bs4 import BeautifulSoup
    d = {}
    html_doc = str(open("all_books.html", "r").readlines())
    soup = BeautifulSoup(html_doc, 'html.parser')
    books = soup.findAll("tr", {"class": "book"})
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
                            stevens_metadata[x] = book_metadata_elm.text
                    book_dict["stevens-metadata"] = stevens_metadata

                    # Parse Book Pricing
                    stevens_pricing = {}
                    for price in book.find_all("td", {"class": "price"}):
                        price_label = price.find("label")
                        book_type = price_label.get("for")[10:].split("_")[0]
                        book_cost = price_label.text
                        if book_cost != "N/A":
                            stevens_pricing[book_type] = float(book_cost[1:])
                    book_dict["stevens-metadata"] = stevens_metadata
                    d[course].append(book_dict)
    return d

print json.dumps(parse_all_books_page(), sort_keys=True, indent=4, separators=(',', ': '))

