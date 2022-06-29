This is the second project in Text Analytics.

Author: Lince Rumainum

Step-by-step instructions for this assignment can be found in: https://oudalab.github.io/textanalytics/projects/project1 

Additional websites to see some examples are in the linked above, and reading and lectures notes from https://oudalab.github.io/textanalytics/schedule.

This program take all the files in the docs folder and redacting them accordingly

all the names in nltk library will be redacted

phones numbers, such as, (XXX) XXX-XXXX, XXX-XXX-XXXX, XXX XXX-XXXX, XXX-XXXX, 4065551234, 5551234

addresses with 1-4 digits number + 1-20 characters street name 
+ street|st|avenue|ave|road|rd|highway|hwy|square|sq|trail|trl|drive|dr|court|ct|park|parkway|pkwy|circle|cir|boulevard|blvd will be redacted

dates, such as, 18 Jan 2000, 18th Jan 2000, 18 January 2000, 18th January 2000, 18/01/2000, 01/18/2000, 01/18/00, 18/01/00 will be redacted

concept that is similar according to nltk.corpus.wordnet will be redacted.
Example: https://www.geeksforgeeks.org/get-synonymsantonyms-nltk-wordnet-python/

External link help:
https://github.com/madisonmay/CommonRegex to see common regex uses

How to run the python code: The framework use for testing the python file: py.test.

Install pytest using the command line: pipenv install pytest

To run the test, on command line type (choose one of the two options): 

pipenv run python -m pytest 

OR

pipenv run python setup.py test