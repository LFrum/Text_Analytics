# test_phones.py
import pytest
import project1
from project1 import redactor


def test_phones():
    # this text file is to test phone redaction
    phoneTestFile = "docs/otherfiles/text-for-phones.txt"
    currInput = open( phoneTestFile )
    strInput = currInput.read()
    currInput.close()

    redactFile, phoneCount = redactor.redactPhones(strInput)
    phones = ["101 555-1234", "(101) 555-1234", "(101)5551234", "101-555-1234", "405 123 4567", "4051234567", "405123-4567"]
    phoneFound = False
    if (redactFile in phones):
    #if (phones in redactFile):
        phoneFound = True

    assert phoneFound == False
    assert phoneCount ==  7