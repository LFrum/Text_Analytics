# -*- coding: utf-8 -*-
# main.py
# https://www.w3schools.com/python/python_file_remove.asp -- remove file

import argparse
import urllib.request
import PyPDF2
import requests
import tempfile
import sqlite3
from sqlite3 import Error 
import pandas as pd
import os
import random
	
def fetchincidents(url):
	# dowmload data from url  
	arrestData = requests.get(url, stream = True) 
	# save data as pdf  - "wb" indicates write in bytes 
	with open("arrestFile.pdf","wb") as pdf:
		# iterate through the data from the url
		for chunk in arrestData.iter_content(chunk_size=65536):	  
			# if there is data, write to the pdf file, else close the file
			if chunk: 
				pdf.write(chunk)
			else:
				pdf.close()
	
	
def extractincidents():
	arrestFile = 'arrestFile.pdf'
	data = open(arrestFile, "rb")
	
	fp = tempfile.TemporaryFile()
	
	# Write the pdf data to a temp file
	fp.write(data.read())
	
	# Set the curser of the file back to the begining
	fp.seek(0)
	
	# Read the PDF
	pdfReader = PyPDF2.PdfFileReader(fp)
	pdfReader.getNumPages()

	page1 = pdfReader.getPage(0).extractText()
	
	# parse page1
	startIndex = page1.find("Officer")
	endIndex1 = page1.rfind("NORMAN POLICE DEPARTMENT")
	endIndex2 = page1.rfind("Daily Arrest Activity (Public)")
	
	# start after officer and exclude end
	if endIndex1 < endIndex2:
		parseData = page1[startIndex + len("Officer") + 1:endIndex1]
	else:
		parseData = page1[startIndex + len("Officer") + 1:endIndex2]
	
	# create new list for data
	newList = []
	# iterate for each line of string
	lines = iter(parseData.splitlines())
	# insert each iteration to the list
	for line in lines:
		newList.append(line)
	
	# initial lists for each data
	time = []
	caseNo = []
	arr_loc = []
	offense = []
	arrestee = []
	arr_birthday = []
	arr_address = []
	arr_status = []
	officer = []	
	tempList = []
	
	currIndex = 0 #index iterator
	while currIndex < len(newList):
		# time
		time.append(newList[currIndex])
		currIndex += 1
		
		# case number
		caseNo.append(newList[currIndex])
		currIndex += 1
		
		# arrest location
		while newList[currIndex][len(newList[currIndex])-1] == ' ':
			tempList.append(newList[currIndex])
			currIndex += 1
		tempList.append(newList[currIndex])
		
		arr_loc.append(''.join(tempList))
		currIndex += 1
		#clear tempList
		tempList.clear()
		del tempList[:]
		tempList = []			
		
		#offense
		while newList[currIndex][len(newList[currIndex])-1] == ' ':
			tempList.append(newList[currIndex])
			currIndex += 1
		tempList.append(newList[currIndex])
		
		offense.append(''.join(tempList))		
		currIndex += 1		
		#clear tempList
		tempList.clear()
		del tempList[:]
		tempList = []
		
		#arrestee
		while newList[currIndex][len(newList[currIndex])-1] == ' ':
			tempList.append(newList[currIndex])
			currIndex += 1
		tempList.append(newList[currIndex])
		
		arrestee.append(''.join(tempList))
		#clear tempList
		tempList.clear()
		del tempList[:]	
		tempList = []
		currIndex += 1
		
		#arrestee birthday			
		arr_birthday.append(newList[currIndex])
		currIndex += 1
		
		#arrestee address
		while 'FDBDC (Jail)' not in newList[currIndex] and 'Municipal Court' not in newList[currIndex] and 'Released- ' not in newList[currIndex]:
			while newList[currIndex][len(newList[currIndex])-1] == ' ':
				tempList.append(newList[currIndex])
				currIndex += 1
				#tempStr = newList[currIndex].strip()
			tempList.append(newList[currIndex])			
			
			currIndex += 1
			#tempStr = newList[currIndex].strip()
		arr_address.append(' '.join(tempList))
		#clear tempList
		tempList.clear()
		del tempList[:]
		tempList = []
		
		#status
		while newList[currIndex][len(newList[currIndex])-1] == ' ':
			tempList.append(newList[currIndex])
			currIndex += 1
		tempList.append(newList[currIndex])
		arr_status.append(''.join(tempList))
		#clear tempList
		tempList.clear()
		del tempList[:]
		tempList = []
		currIndex += 1
		
		#officer
		while newList[currIndex][len(newList[currIndex])-1] == ' ':
			tempList.append(newList[currIndex])
			currIndex += 1
		tempList.append(newList[currIndex])
		officer.append(''.join(tempList))
		#clear tempList
		tempList.clear()
		del tempList[:]
		tempList = []
		currIndex += 1

	# put all the data into a dictionary
	dataDict = {'Time': time, 'CaseNum':caseNo, 'ArrestLocation': arr_loc, 'Offense': offense, 'Arrestee':arrestee, 
		'ArresteeBirthday': arr_birthday,'ArresteeAddress': arr_address,'Status': arr_status,'Officer': officer}
	
	# create data frame from the data
	df = pd.DataFrame(dataDict)

	#close pdf file
	data.close()
	return df
	
def createdb():
	# create database file
	database_file = "./normanpd.db"
	
	# create a database connection
	conn = create_db_connection(database_file)
	
	# setup arrests table
	sql_create_arrests_table = """ CREATE TABLE IF NOT EXISTS arrests (
								arrest_time TEXT,
								case_number TEXT,
								arrest_location TEXT,
								offense TEXT,
								arrestee_name TEXT,
								arrestee_birthday TEXT,
								arrestee_address TEXT,
								status TEXT,
								officer TEXT
							); """
							
	if conn is not None:
		# create arrests table		
		try:
			c = conn.cursor()
			c.execute(sql_create_arrests_table)
		except Error as e:
			print(e)	
	else:
		print("Error! cannot create the database connection.")
		
	# close database connection
	conn.close()
	
	return database_file
	
def populatedb(db, incidents):
	# create a database connection
	conn = create_db_connection(db)
	
	with conn:
		# enter each incident into the database
		for index, row in incidents.iterrows():
			# create a new incident
			incident = (row['Time'], row['CaseNum'],row['ArrestLocation'],
				row['Offense'], row['Arrestee'],row['ArresteeBirthday'],
				row['ArresteeAddress'],row['Status'],row['Officer'])

			sql = ''' INSERT INTO arrests(arrest_time, case_number, arrest_location, offense, 
					arrestee_name, arrestee_birthday, arrestee_address, status, officer)
					VALUES(?,?,?,?,?,?,?,?,?) '''
			cur = conn.cursor()
			cur.execute(sql, incident)
	
	# close database connection
	conn.close()	

def status(db):
	# create a database connection
	conn = create_db_connection(db)
	
	if conn is not None:		
		cur = conn.cursor()
		# select random incident and output to console
		randomIncident = cur.execute("SELECT * FROM arrests ORDER BY RANDOM() LIMIT 1").fetchone()

		index = 0
		tempList = []
		# create a list from tuple randomIncident
		while index < len(randomIncident):
			tempList.append(randomIncident[index])
			lastCharIndex = len(randomIncident[index]) - 1
			if randomIncident[index][lastCharIndex] != ';' :
				tempList.append('þ')
			index += 1
		# join tempList to print off each field of the database row 
		# separated by the thorn character (þ)
		incident = ''.join(tempList)
		print (incident)
		
	else:
		print("Error! cannot create the database connection.")
	
	# close database connection
	conn.close()
	return incident	
		
def create_db_connection(db_file):	
	# create a database connection
	try:
		#conn = sqlite3.connect(':memory:')
		conn = sqlite3.connect(db_file)
		return conn
	except Error as e:
		print(e)	

def removeDB(db_file):
    #remove database
    os.remove(db_file)