""" Courtses tools """
from app import mongo_client

DEPARTMENTS = {
    "BIA": "Business Intelligence and Analytics",
    "BIO": "Biology",
    "BME": "Biomedical Engineering",
    "BT": "Business and Technology",
    "CAL": "College of Arts & Letters",
    "CE": "Civil Engineering",
    "CH": "Chemistry and Chemical Biology",
    "CHE": "Chemical Engineering",
    "CM": "Construction Management",
    "CPE": "Computer Engineering",
    "CS": "Computer Science",
    "D": "Dean's Offices",
    "E": "Interdepartmental Engineering",
    "EE": "Electrical Engineering",
    "EM": "Engineering Management",
    "EN": "Environmental Engineering",
    "ES": "Enterprise Systems",
    "FE": "Financial Engineering",
    "FIN": "Finance",
    "H": "Honor Program",
    "HAR": "Humanities/Art",
    "HHS": "Humanities/History",
    "HLI": "Humanities/Literature",
    "HMU": "Humanities/Music",
    "HPL": "Humanities/Philosophy",
    "HSS": "Humanities/Social Sciences",
    "HST": "Humanities/Science and Technology",
    "HTH": "Humanities/Theater",
    "IDP": "Integrated Product Development",
    "LFR": "Language/French",
    "LSP": "Language/Spanish",
    "MA": "Mathematics",
    "ME": "Mechanical Engineering",
    "MGT": "Management",
    "MIS": "Information Systems",
    "MT": "Materials Science and Engineering",
    "NANO": "Nanotechnology",
    "NE": "Naval Engineering",
    "NIS": "Networked Information Systems",
    "OE": "Ocean Engineering",
    "PAE": "Product Architecture and Engineering",
    "PE": "Physical Education",
    "PEP": "Physics & Engineering Physics",
    "PIN": "Pinnacle Scholar",
    "PME": "Pharmaceutical Manufacturing",
    "PRV": "Provost",
    "QF": "Quantitative Finance",
    "REG": "Registrar",
    "SDOE": "Systems Design and Operational Effectiveness",
    "SEF": "Science & Engineering Found. for E",
    "SES": "Systems Engineering Security",
    "SOC": "Service Oriented Computing",
    "SSW": "Software Engineering",
    "SYS": "Systems Engineering",
    "TG": "Technogenesis",
    "TM": "Telecommunications Management"
}


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
    return mongo_client.catalog.courses.find_one({"letter": letter.upper(), "number": number})


def get_books_by_course(letter, number):
    """ Get books by course
    :return:
    """
    return mongo_client.ssw695.books.find({"courses.letter": letter.upper(), "courses.number": number})
