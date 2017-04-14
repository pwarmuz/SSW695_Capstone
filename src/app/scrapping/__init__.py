import stevens_bookstore
import google_books

from app import mongo_client

def update_book_with_google_metadata(isbn):
    r = google_books.get_info_by_isbn(isbn)
    if r["success"]:
        if r["data"] is None:
            print("books not found in google api")
        else:
            mongo_client["ssw695"]["books"].update_one({"_id": isbn}, {"$set": {"google-metadata": r["data"]}},
                                                       upsert=True)
    else:
        print("google api error", r)


def update_all_books_with_google_metadata():
    for x in mongo_client["ssw695"]["books"].find({}):
        update_book_with_google_metadata(x["_id"])

