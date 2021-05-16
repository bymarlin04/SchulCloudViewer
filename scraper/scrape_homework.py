import requests
import hashlib

from .helpers import make_soup, get_course_name, get_created_due_date, Assignment
from . import log
from .vars import vars

def get_homeworks(session: requests.Session, csrf: str, cookies: str, user_id: str) -> list:
    """Scrapes all available assignments on a given URL"""
    log.debug(f"Getting assignments for {csrf}")
    homework_soup = make_soup(session.get(vars.HOMEWORK_URL, cookies=cookies, data={"_csrf":csrf}).text)
    homeworks = homework_soup.find_all('li', class_="assignment")

    homework_objects = []
    for homework in homeworks:
        link = homework.find('a')
        link = link.attrs['href'].strip("\n\t ")
        link = vars.URL + link

        homework_objects.append(get_homework(session, link, csrf, cookies, user_id))

    return homework_objects

def get_homework(session: requests.Session, url: str, csrf: str, cookies, user_id) -> Assignment:
    """Extracts the information from an assignment URL"""
    homework = session.get(url, cookies=cookies, data=csrf)
    
    homework_soup = make_soup(homework.text)

    course = get_course_name(homework_soup.title.string)[0]
    name = get_course_name(homework_soup.title.string)[1]

    log.debug(f"New assignment: {course} % {name} (ID: {csrf})")

    description = homework_soup.find_all('div', class_='description')[0]
    description = description.find_all('div')[1]

    log.debug(f"Description: {description}")

    date_string = homework_soup.find_all('div', class_='dates')
    created_date = get_created_due_date(date_string[0].text)[0]
    due_date = get_created_due_date(date_string[0].text)[1]

    done = True if homework_soup.find('i', class_="done") is not None else False

    log.debug(f"Done: {done}")

    return Assignment(name, course, url, description, due_date, created_date)