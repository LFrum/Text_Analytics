# test_stats.py
import pytest
import project1
from project1 import redactor
import pandas as pd

def test_stats():
    #python redactor.py --input '*.txt' --input 'otherfiles/*.txt' --names --dates --addresses --phones --concept 'kids' --output 'files/' --stats stderr
    inputFiles = []
    inputFiles.append('*.txt')
    inputFiles.append('otherfiles/*.txt')  

    print ("inputFiles ", inputFiles)
    allInputs = redactor.getInputFiles(inputFiles)
    print (allInputs)
    
    names = True
    dates = True
    addresses = True
    phones = True
    concept = 'kids'
    output = 'files/'
    statsOutput = str('stderr')

    # Extract Data and return data frame of stats
    print("allInputs: ",allInputs)
    statsData = redactor.redactData(allInputs, names, dates, addresses, phones, concept, output)

    inputFiles =["docs/text-for-all.txt","docs/text-for-dates.txt","docs/text-for-names.txt",
                "docs/otherfiles/text-for-addresses.txt","docs/otherfiles/text-for-concepts.txt",
                "docs/otherfiles/text-for-phones.txt"]
    namesCount = [5, 0, 10, 2, 0, 0]
    datesCount = [1, 7, 0, 0, 0, 0]
    addressesCount = [1,0, 0, 8, 0, 0]
    phonesCount = [1, 0, 0, 0, 0, 7]
    conceptsCount = [7, 2, 2, 2, 3, 2]

    # put all the data into a dictionary
    dataDict = {'File': inputFiles, 'countNames':namesCount, 'countDates': datesCount, 'countAddress': addressesCount,
        'countPhones': phonesCount,'countConcepts': conceptsCount}

    # create data frame from the data
    df = pd.DataFrame(dataDict)

    print("statsData: ", statsData)
    print("df: ", df)
    isStatsGood = False
    isStatsGood = pd.DataFrame.equals(statsData, df)
    assert isStatsGood == True