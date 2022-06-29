# redactor.py
# -*- coding: utf-8 -*-

#import project1
import argparse
import sys
import _io
import tempfile
import pandas as pd
import os
import glob
import re
import nltk
from nltk.corpus import stopwords
from nltk.corpus import wordnet
from nltk.stem import WordNetLemmatizer   
import nltk.tokenize.regexp                                                                 
from nltk.tokenize.regexp import RegexpTokenizer 
from nltk import SnowballStemmer  
from nltk.corpus import names  
from nltk import word_tokenize, pos_tag, ne_chunk
from nltk.corpus import wordnet
from commonregex import CommonRegex
import os  

def main (inputFiles, names, dates, addresses, phones, concept, output, statsOutput):
    # get all input text files
    allInputs = getInputFiles(inputFiles)
    #print(type(sys.stderr))
    # Extract Data and return data frame of stats
    statsData = redactData(allInputs, names, dates, addresses, phones, concept, output)
    #print ("statsData: ", statsData)
    #print ("back in main")
    statsOutput = str(statsOutput)
    # show stats
    printStats(statsOutput, statsData)

def getInputFiles(input):
    #print ("getInputFiles FUNCTION")
    allFiles = []
    inputFiles = []
    for i in range(0,len(input)):
        # get only string text only
        input[i] = input[i].replace("'","")
        # get all input files from specified directory
        #inputFiles = glob.glob('../docs/' + input[i]) # use this when run directly from project1 folder
        inputFiles = glob.glob('docs/' + input[i]) # use this to run test
        
        # get filename
        for i in range(0,len(inputFiles)):
            allFiles.append(inputFiles[i])			

    #print ("END getInputFiles FUNCTION")
    return allFiles

def createOutputFiles(outputFolder, inputFile, redactedFile):    
    output = outputFolder
    # create output from the redacted file 
    #print ("output file BEFORE: ", output)
    output = output.replace("'","")
    #output = '../' + output
    #print ("output file AFTER: ", output)
    if os.path.isdir(output) == False:
        os.mkdir(output)
    currOutputName = inputFile.replace("../docs/", output)    
    currOutputName = inputFile.replace("docs/", output)
    #print ("currOutputName: ", currOutputName)
    currOuputDir, currFile = os.path.split(currOutputName)
    if os.path.isdir(currOuputDir) == False:
        os.makedirs(currOuputDir)
    currOutputName = currOutputName.replace(".txt", ".redacted.txt")
    currOutput = open(currOutputName, "w", encoding='utf-8')
    currOutput.write("%s" % redactedFile)
    currOutput.close()

# redact data and put it into an output file
def redactData(specifiedFiles, names, dates, addresses, phones, concept, output):
    inputFiles = []
    statList = []
    # redacted count in a list for each file  
    namesCount = []
    datesCount = []
    addressesCount = []
    phonesCount = []
    conceptsCount = []

    stop = stopwords.words('english')

    for i in range(0,len(specifiedFiles)):
        # initialize count stats
        nameCount = 0
        dateCount = 0
        addressCount = 0
        phoneCount = 0
        conceptCount = 0

        specifiedFiles[i] = specifiedFiles[i].replace("\\","/")
        inputFiles.append(specifiedFiles[i])
        currInput = open( specifiedFiles[i] )
        strInput = currInput.read()
        currInput.close()        
        #print(strInput)

        redactedFile_names = ""
        if (names == True):
            redactedFile_names, nameCount = redactNames(strInput)
            namesCount.append(nameCount)
            #print("redactedFile_names: ", redactedFile_names)
        if (redactedFile_names != ""):
            strInput = redactedFile_names

        redactedFile_dates = ""
        if (dates == True):
            redactedFile_dates, dateCount = redactDates(strInput)            
            #print("redactedFile_dates: ", redactedFile_names)
            datesCount.append(dateCount)
        if (redactedFile_dates != ""):
            strInput = redactedFile_dates
        
        redactedFile_addresses = ""
        if (addresses == True):
            redactedFile_addresses, addressCount = redactAddresses(strInput)            
            #print("redactedFile_addresses: ", redactedFile_addresses)
            addressesCount.append(addressCount)
        if (redactedFile_addresses != ""):
            strInput = redactedFile_addresses

        redactedFile_phones = ""
        if (phones == True):
            redactedFile_phones, phoneCount = redactPhones(strInput)            
            #print("redactedFile_phones: ", redactedFile_phones)
            phonesCount.append(phoneCount)
        if (redactedFile_phones != ""):
            strInput = redactedFile_phones

        redactedFile_concept = ""
        if (concept.strip() != ""):
            redactedFile_concept, conceptCount = redactConcept(strInput, concept)            
            #print("redactedFile_concept: ", redactedFile_concept)
            conceptsCount.append(conceptCount)
        if (redactedFile_concept != ""):
            strInput = redactedFile_concept

        redactedFile = strInput
        # create output from the redacted file 
        createOutputFiles(output, specifiedFiles[i], redactedFile)
        
    # put all the data into a dictionary
    dataDict = {'File': inputFiles, 'countNames':namesCount, 'countDates': datesCount, 'countAddress': addressesCount,
        'countPhones': phonesCount,'countConcepts': conceptsCount}

    # create data frame from the data
    df = pd.DataFrame(dataDict)
    #print (df)

    return df
    #return statList

def redactNames(currInputFile):
    countNames = 0
    currDoc = currInputFile
    stop = stopwords.words('english')

    # find the names
    names = []

    strInput = ' '.join([i for i in currInputFile.split() if i not in stop])
    sentences = nltk.sent_tokenize(strInput)
    sentences = [nltk.word_tokenize(sent) for sent in sentences]
    sentences = [nltk.pos_tag(sent) for sent in sentences]

    for tagged_sentence in sentences:
        for chunk in nltk.ne_chunk(tagged_sentence):
            if type(chunk) == nltk.tree.Tree:
                if chunk.label() == 'PERSON':
                    #names.append(' '.join([c[0] for c in chunk]))
                    name = ' '.join([c[0] for c in chunk])
                    names.append(name)
    #print ("names: ", names)

    # redacting the names
    for i in names:
        newSentence = ""
        for j in word_tokenize(i):
            redacted = u"\u2588"*len(j)
            redacted +=" "
            newSentence += redacted
        newSentence = newSentence[:-1]
        currDoc = currDoc.replace(i, redacted)
    #print(names)
    # total name redacted    
    countNames = len(names)
    #return textWithRedactedName
    #result = [currDoc, countNames]
    return currDoc, countNames

def redactDates(currInputFile):
    countDates = 0
    currDoc = currInputFile
    dates = []
    parsed_text = CommonRegex (currDoc)
    dates = parsed_text.dates

    # redacting the dates
    for i in dates:
        newSentence = ""
        for j in word_tokenize(i):
            redacted = u"\u2588"*len(j)
            redacted +=" "
            newSentence += redacted
        newSentence = newSentence[:-1]
        currDoc = currDoc.replace(i, redacted)

    # total dates redacted    
    countDates = len(dates)
    #return textWithRedactedDate
    return currDoc, countDates

def redactAddresses(currInputFile):
    countAddresses = 0
    currDoc = currInputFile
    addresses = []
    #addresses = re.findall(r'\d{1,4} [\w\s]{1,20}(?:street|st|avenue|ave|road|rd|highway|hwy|square|sq|trail|trl|drive|dr|court|ct|park|parkway|pkwy|circle|cir|boulevard|blvd)\W?(?=\s|$)', strInput)
    addresses = re.findall(r'\d{1,4} [\w\s]{1,20}(?:street|Street|st|St|avenue|Avenue|ave|Ave|road|Road|rd|Rd|highway|Highway|hwy|Hwy|square|Square|sq|Sq|trail|Trail|trl|Trl|drive|Drive|dr|Dr|court|Court|ct|Ct|park|Park|parkway|Parkway|pkwy|Pkwy|circle|Circle|cir|Cir|boulevard|Boulevard|blvd|Blvd)\W?(?=\s|$)', currDoc)

    # redacting the addresses
    for i in addresses:
        newSentence = ""
        for j in word_tokenize(i):
            redacted = u"\u2588"*len(j)
            redacted +=" "
            newSentence += redacted
        newSentence = newSentence[:-1]
        currDoc = currDoc.replace(i, redacted)

    # total addresses redacted    
    countAddresses = len(addresses)
    #return textWithRedactedAddresses
    return currDoc, countAddresses

def redactPhones(currInputFile):
    countPhones = 0
    currDoc = currInputFile
    phones = []
    phones = re.findall(r'''((?:(?<![\d-])(?:\+?\d{1,3}[-.\s*]?)?(?:\(?\d{3}\)?[-.\s*]?)?\d{3}[-.\s*]?\d{4}(?![\d-]))|(?:(?<![\d-])(?:(?:\(\+?\d{2}\))|(?:\+?\d{2}))\s*\d{2}\s*\d{3}\s*\d{4}(?![\d-])))''', currDoc)

    # redacting the phones
    for i in phones:
        newSentence = ""
        for j in word_tokenize(i):
            redacted = u"\u2588"*len(j)
            redacted += " "
            newSentence += redacted
        newSentence = newSentence[:-1]
        currDoc = currDoc.replace(i, redacted)

    # total phones redacted    
    countPhones = len(phones)
    #return textWithRedactedPhones
    return currDoc, countPhones

# optional
def redactGender(currInputFile):
	#return textWithRedactedGender
	pass

# concept still not working
def redactConcept(currInputFile, concept):
    conceptCount = 0
    currDoc = currInputFile    
    all_concepts = []
    synonyms = []
    
    # take out '' from concept string
    concept = concept.replace("'","") 
    for synonym in wordnet.synsets(concept):        
        for listOfSyn in synonym.lemmas():
            currSyn = listOfSyn.name()
            # replace underscore with space 
            currSyn = currSyn.replace('_', ' ')
            synonyms.append(currSyn)
    #print(synonyms)
    
    # redacting the concepts
    for i in synonyms:
        newSentence = ""
        #print ("word_tokenize(i)",word_tokenize(i))
        for j in word_tokenize(i):
            redacted = u"\u2588"*len(j)
            redacted += " "
            newSentence += redacted
        newSentence = newSentence[:-1]
        currDoc = currDoc.replace(i, redacted)

    for k in currDoc.split('.'):
        #print("k: ",k)

        if (u"\u2588" in k):
            conceptCount += 1
            redacted = u"\u2588"*len(k)
            redacted += " "
            currDoc = currDoc.replace(k, redacted)

    return currDoc, conceptCount
	
# create stats
def printStats(statsOutput, statsData):
    # statsData is in a dataframe
    
    #dataDict = {'File': inputFiles, 'countNames':namesCount, 'countDates': datesCount, 'countAddress': addressesCount,
    #    'countPhones': phonesCount,'countConcepts': conceptsCount}
    outputText = ""
    numOfRow = statsData.shape[0]
    for i in range(0,numOfRow):
        if i > 0:
            outputText += "\n"
        colNum = 0
        outputText += "In " + str(statsData.iloc[i, colNum]) + ":\n"
        colNum += 1
        outputText += "There is/are " + str(statsData.iloc[i, colNum]) + " name(s) was redacted.\n"
        colNum += 1
        outputText += "There is/are " + str(statsData.iloc[i, colNum]) + " date(s) was redacted.\n"
        colNum += 1
        outputText += "There is/are " + str(statsData.iloc[i, colNum]) + " address(es) was redacted.\n"
        colNum += 1
        outputText += "There is/are " + str(statsData.iloc[i, colNum]) + " phone(s) was redacted.\n"
        colNum += 1
        outputText += "There is/are " + str(statsData.iloc[i, colNum]) + " concept(s) was redacted.\n"
        #print(outputText)

    # stderr output
    if (statsOutput == "stderr"):
        print (outputText, file = sys.stderr)
    # stdout output
    elif (statsOutput == "stdout"):
        print (outputText, file = sys.stdout)
    # file output
    else: 
        output = statsOutput
        output = output.replace("'","")
        if os.path.isdir(output) == False:
            os.mkdir(output)
        currOutputName = "../files/" + output
        #currOutputName = inputFile.replace("../docs/", output)    
        #currOutputName = inputFile.replace("docs/", output)        
        currOuputDir, currFile = os.path.split(currOutputName)
        #print ("currOuputDir: ", currOuputDir)
        if os.path.isdir(currOuputDir) == False:
            os.makedirs(currOuputDir)
        #currOutputName = currOutputName.replace(".txt", ".redacted.txt")
        currOutput = open(currOutputName, "w", encoding='utf-8')
        currOutput.write("%s" % outputText)
        currOutput.close()
    return outputText
    # output the stats
    #pass

if __name__ == '__main__':
	# get each arguments: input, flags (names, dates, address, phones), concept, output, and stats
	parser = argparse.ArgumentParser()
	parser.add_argument("--input", type=str,action='append', required=True, 
						help="Input files from directory.")

	parser.add_argument("--names", action='store_true',
						help="Names in file need to be redacted.")
	
	parser.add_argument("--dates", action='store_true',
						help="Dates in file need to be redacted.")
	
	parser.add_argument("--addresses", action='store_true',
						help="Addresses in file need to be redacted.")	
		
	parser.add_argument("--phones", action='store_true',
						help="Phones in file need to be redacted.")	

	parser.add_argument("--concept", type=str, required=True, 
						help="Concept data in file need to be redacted.")
		
	parser.add_argument("--output", type=str, required=True, 
						help="Output data from files.")
		
		
	parser.add_argument("--stats", required=True, 
						help="Stats data printed out to a file in files folder or stderr stdout.")
	
		
	args = parser.parse_args()
	
	if args.input:
		inputFiles = args.input	
		
	if args.names:
		names = args.names
	
	if args.dates:
		dates = args.dates
	
	if args.addresses:
		addresses = args.addresses
		
	if args.phones:
		phones = args.phones	
		
	if args.concept:
		concept = args.concept
		
	if args.output:
		outputFiles = args.output
		
	if args.stats:
		stats = args.stats
		
	# take all input into main
	main (inputFiles, names, dates, addresses, phones, concept, outputFiles, stats)