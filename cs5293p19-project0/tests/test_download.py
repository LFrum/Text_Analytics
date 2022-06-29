import pytest
import project0
from project0 import __init__
import os

url = ("http://normanpd.normanok.gov/filebrowser_download/657/2019-02-21%20Daily%20Arrest%20Summary.pdf")

def test_download_sanity():
	project0.fetchincidents(url)
	isFileDownloaded = os.path.exists('./arrestFile.pdf')
	assert isFileDownloaded is True