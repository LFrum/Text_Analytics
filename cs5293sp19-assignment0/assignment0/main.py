import json
import random
import urllib.request

# Python3 type hints
# https://mypy.readthedocs.io/en/latest/cheat_sheet_py3.html
from typing import List, Dict, Any

url = "https://raw.githubusercontent.com/TrumpTracker/trumptracker.github.io/master/_data/data.json"


def download():
    """ This function downloads the json data from the url."""
    # TODO add code here
    # open and download the url content
    response = urllib.request.urlopen(url)
    # read the content into string
    data = response.read()
    return data


def extract_requests(text: str) -> List[Dict[str, Any]]:
    """
        This function turns the json data into a dict object and
        extracts and returns the array of promises.
    """
    # TODO add code here
    # convert the string file into json file
    jsonData = json.loads(text)
    # use promises as key and store it into the list
    promisesList = jsonData['promises']
    return promisesList


def extract_titles(promises: List[Dict[str, Any]]) -> List[str]:
    """ Make a new array with just the titles. """
    # TODO add code here
    # create list of titles from promises list
    titleList = [i['title'] for i in promises]
    return titleList


def random_title (titles: List[str]) -> str:
    """ This function takes list of titles and returns one string at random. """
    # TODO add code here
    # pick random title from the list of titles
    title = random.choice(titles)
    return title
