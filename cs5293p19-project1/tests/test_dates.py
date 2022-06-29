# test_dates.py
import pytest
import project1
from project1 import redactor


def test_dates():    
    # this text file is to test date redaction
    dateTestFile = "docs/text-for-dates.txt"
    currInput = open( dateTestFile )
    strInput = currInput.read()
    #print (strInput)
    currInput.close()

    redactFile, dateCount = redactor.redactDates(strInput)
    dates = ["1 January 2019 ", "January 1st, 2019", " 1/1/2019", "01/01/2019", "18/03/2018", "03/30/2020", "3/30/20"]
    dateFound = False
    if (redactFile in dates):
    #if (dates in redactFile):
        dateFound = True

    assert dateFound == False
    assert dateCount ==  7