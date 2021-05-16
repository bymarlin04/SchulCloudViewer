import requests
import hashlib

from .login import login, get_csrf
from .scrape_homework import get_homeworks
from . import log
from .vars import vars

def scrape_tasks(username: str, password: str, vars: object = vars) -> any:
    """Scrapes the tasks for a particular user with username and password; returns a dict"""
    sha = hashlib.shake_256(bytes(username, "utf8"))
    user_id = sha.hexdigest(32)

    log.debug(f"Scraping tasks for {user_id}...")
    s = requests.Session()

    # Checking for errors and getting the CSRF token
    login_page = s.get(vars.LOGIN_URL)
    csrf = get_csrf(login_page.text)
    
    login(s, username, password, csrf, login_page.cookies)
    assignments = get_homeworks(s, csrf, login_page.cookies, user_id)

    return assignments