# test_name.py
import pytest
import project1
from project1 import redactor

def test_names():
    # this text file is to test name redaction
    nameTestFile = "docs/text-for-names.txt"
    currInput = open( nameTestFile )
    strInput = currInput.read()
    currInput.close()

    redactFile, nameCount = redactor.redactNames(strInput)
    #print (redactFile)
    names = ["John", "Jane", "Richard", "Stefani", "Emma Watson", "Danny DeVito", "Jon", "Larry", "Nick", "Paul"]
    nameFound = False
    if (redactFile in names):
    #if (names in redactFile):
        nameFound = True

    assert nameFound == False
    assert nameCount ==  10