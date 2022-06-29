import pytest
import project0
from project0 import __init__
import pandas as pd
import sqlite3
from sqlite3 import Error 

# this url might need to be updated
url = ("http://normanpd.normanok.gov/filebrowser_download/657/2019-05-05%20Daily%20Arrest%20Summary.pdf")

def test_extract_data():
    # Download data
	project0.fetchincidents(url)

	# Extract Data
	incidents = project0.extractincidents()

	assert type(incidents) == pd.core.frame.DataFrame
	assert len(incidents) > 0
	
def test_create_database():
	# Download data
	project0.fetchincidents(url)

	# Extract Data
	incidents = project0.extractincidents()

	# Create Dataase
	db = project0.createdb()

	databaseError = False
	# create a database connection
	try:
		conn = sqlite3.connect(db)
	except Error as e:
		databaseError = True
		print(e)	
	finally:
		conn.close()
	assert databaseError == False
	#remove database
	project0.removeDB(db)


def test_insert_data():
	# Download data
	project0.fetchincidents(url)
	# Extract Data
	incidents = project0.extractincidents()
	# Create Dataase
	db = project0.createdb()
	# Insert Data
	project0.populatedb(db, incidents)
	
	# create a database connection
	conn = project0.create_db_connection(db)
	
	if conn is not None:		
		cur = conn.cursor()
		# select all incidents
		incidents = cur.execute("SELECT * FROM arrests").fetchall()
	else:
		print("Error! cannot create the database connection.")
	
	# close database connection
	conn.close()

	assert type(incidents) == list
	#remove database
	project0.removeDB(db)

def test_random_status():
	# Download data
	project0.fetchincidents(url)
	# Extract Data
	incidents = project0.extractincidents()
	# Create Dataase
	db = project0.createdb()
	# Insert Data
	project0.populatedb(db, incidents)
	# Print Status
	data = project0.status(db)
	assert type(data) == str
	assert data.count('þ') == 8
	#remove database
	project0.removeDB(db)