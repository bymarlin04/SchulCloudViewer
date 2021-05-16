from bs4 import BeautifulSoup
import requests
import re

from . import log
from .helpers import make_soup, LoginError
from .vars import vars

def get_csrf(page: str) -> str:
    """Extracts the CSRF token from the login page"""
    soup = make_soup(page)
    csrf = soup.find_all('input', attrs={'name': '_csrf'})
    return csrf[0].attrs['value']

def login(session: requests.Session, username: str, password: str, csrf: str, cookies, url: str = vars.LOGIN_URL) -> None:
    """Logs the user into the SchulCloud for further access to data."""
    log.debug(f"Trying to log in as {csrf}")

    payload = {'username': username, 'password': password, '_csrf': csrf}
    with session.post(url, cookies=cookies, data=payload, allow_redirects=True) as response:
        soup = make_soup(response.text)
        title_expression = re.compile('Übersicht[\s\w]')
        if title_expression.match(str(soup.title.string)) is None:
            log.error(f"Login failure as {csrf}")
            raise LoginError("Login failure, wrong credentials?")

    log.debug(f"Login successful as {csrf}")