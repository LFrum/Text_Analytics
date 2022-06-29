# test_concept.py
import pytest
import project1
from project1 import redactor

def test_concepts():
    # this text file is to test concept redaction
    concept = "kids"
    conceptTestFile = "docs/otherfiles/text-for-concepts.txt"
    currInput = open( conceptTestFile )
    strInput = currInput.read()
    currInput.close()

    redactFile, conceptCount = redactor.redactConcept(strInput, concept)
    print (redactFile)
    concepts = ["kids","youngster", "child"]
    conceptFound = False
    if (redactFile in concepts):
    #if (concepts in redactFile):
        conceptFound = True

    assert conceptFound == False
    assert conceptCount ==  3