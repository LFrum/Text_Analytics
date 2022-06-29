This is the first project in Text Analytics.

Author: Lince Rumainum

Step-by-step instructions for this assignment can be found in: https://oudalab.github.io/textanalytics/projects/project0 

Additional websites to see some examples are in the linked above, and reading and lectures notes from https://oudalab.github.io/textanalytics/schedule.

The program get a pdf file from the arrest data of Norman Police Department. 

It parse data to where the data match for each column seperately, then combine and store it into data frame. 

Then, the program create a database and populate the data from the data frame. It will also give one random data at the end.

How to run the python code: The framework use for testing the python file: py.test.

Install pytest using the command line: pipenv install pytest

To run the test, on command line type (choose one of the two options):

pipenv run python -m pytest 

OR

pipenv run python setup.py test