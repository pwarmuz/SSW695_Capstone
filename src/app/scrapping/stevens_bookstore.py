#!/usr/bin/python
""" Module For Scraping Stevens Bookstore """
import time
import platform
import pickle

import requests
from selenium import webdriver


__author__ = "Constantine Davantzis"
__status__ = "Development"

WINDOWS32_GECKODRIVER_PATH = "webdrivers/geckodriver-v0.14.0-win32/geckodriver"
WINDOWS64_GECKODRIVER_PATH = "webdrivers/geckodriver-v0.14.0-win64/geckodriver"
LINUX32_GECKODRIVER_PATH = "webdrivers/geckodriver-v0.14.0-linux32/geckodriver"
LINUX64_GECKODRIVER_PATH = "webdrivers/geckodriver-v0.14.0-linux64/geckodriver"


def get_geckodriver_path():
    system_name = platform.system()
    is_64_bit = platform.machine().endswith('64')

    if system_name == "Windows":
        return WINDOWS64_GECKODRIVER_PATH if is_64_bit else WINDOWS32_GECKODRIVER_PATH
    return LINUX64_GECKODRIVER_PATH if is_64_bit else LINUX32_GECKODRIVER_PATH


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



#r = requests.post('http://www.stevenscampusstore.com/textbook_express.asp?mode=2&step=2', data={'sectionIds': get_book_id_list()})
#with open("all_books.html", "w") as text_file:
#    text_file.write(r.content)
#from bs4 import BeautifulSoup

#html_doc = str(open("all_books.html", "r").readlines())
#soup = BeautifulSoup(html_doc, 'html.parser')
#books = soup.findAll("tr", {"class": "book"})

#for isbn in soup.findAll("input", {"name": "isbn-1"}):
#    print isbn

