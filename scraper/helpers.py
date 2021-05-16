from bs4 import BeautifulSoup
from .vars import vars

def make_soup(text: str):
    return BeautifulSoup(text, vars.BS_PARSER)

class LoginError(Exception):
    pass

class Assignment(object):
    def __init__(self, name, course, url, description, due_date, created_date):
        self.name = name
        self.course = course
        self.url = url
        self.description = description
        self.due_date = due_date
        self.created_date = created_date

    def __repr__(self):
        return f'<Assignment {self.name} in {self.course}>'

def get_course_name(title: str):
    """Extracts the name and course from a string in format (course) - (title)"""
    title = title.split(" - ")

    course = title[0]
    name = ""

    for s in title[1:-1]:
        s = s.strip()
        if name == "":
            name = f"{s}"
        else:
            name = f"{name} - {s}"

    return [course, name]

def get_created_due_date(date_string: str) -> list:
    """Extracts the date of creation and due date from a string"""
    date_string = date_string.strip()
    date_string = date_string.split(" ")
    
    created_date = f"{date_string[0]} {date_string[1]}"

    due_date = ""
    for s in date_string[2:]:
        if due_date == "":
            due_date = s
        else:
            due_date = due_date + " " + s
    
    return [created_date, due_date]