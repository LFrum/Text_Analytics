# test_output.py
import pytest
import project1
from project1 import redactor
import os

def test_output():
    outputDir = 'files/'
    testFile = "docs/text-for-all.txt"
    currInput = open( testFile )
    strInput = currInput.read()
    currInput.close()

    redactFile, addressCount = redactor.redactAddresses(strInput)
    redactFile, nameCount = redactor.redactNames(redactFile)
    redactFile, phoneCount = redactor.redactPhones(redactFile)
    redactFile, dateCount = redactor.redactDates(redactFile)

    redactor.createOutputFiles(outputDir, testFile, redactFile)

    isFileExist = os.path.exists('files/text-for-all.redacted.txt')
    assert isFileExist is True