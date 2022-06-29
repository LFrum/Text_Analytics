import pytest

import assignment0
from assignment0 import main


def test_extract_request():
    text = main.download()
    promises = main.extract_requests(text)
    assert len(promises) == 174


title0 = "Propose a Constitutional Amendment to impose term limits on all members of Congress"
def test_extract_titles():
    text = main.download()
    promises = main.extract_requests(text)
    titles = main.extract_titles(promises) 

    assert titles[0] == title0


def test_random_title():
    text = main.download()
    promises = main.extract_requests(text)
    titles = main.extract_titles(promises) 
    randomtitle = main.random_title(titles)

    assert type(randomtitle) == str
    assert len(randomtitle) > 0
