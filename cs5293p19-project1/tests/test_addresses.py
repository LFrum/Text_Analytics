# test_addresses.py
import pytest
import project1
from project1 import redactor


def test_addresses():
    # this text file is to test address redaction
    addressTestFile = "docs/otherfiles/text-for-addresses.txt"
    currInput = open( addressTestFile )
    strInput = currInput.read()
    currInput.close()

    redactFile, addressCount = redactor.redactAddresses(strInput)
    print (redactFile)
    addresses = ["101 North Boulevard", "101 N Blvd", "101 N Boulevard", "101 North Blvd", "24 Mullholand Drive", 
        "35 Pico Street", "18 Melrose Avenue", "5th Street", "2 Boyd St", "3 Boyd Street"]
    addressFound = False
    if (redactFile in addresses):
    #if (addresses in redactFile):
        addressFound = True

    assert addressFound == False
    assert addressCount ==  10