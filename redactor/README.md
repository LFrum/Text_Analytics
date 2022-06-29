This is the final project in Text Analytics.

Author: Lince Rumainum

Step-by-step instructions for this assignment can be found in: https://oudalab.github.io/textanalytics/projects/project2 Additional websites to see some examples are in the linked above, and reading and lectures notes from https://oudalab.github.io/textanalytics/schedule.

The program get its data for training and testing from http://ai.stanford.edu/~amaas/data/sentiment/
Download their data set and extract the files from the tarball file:
aclImdb_v1.tar.gz (downloaded file name might be different).
(Note that any folder over 1000 files will only have maximum of 1000 files for each folder in Github)
For training, their dataset have the supervised (positive and negative) and the unsupervised dataset.
Their README file talks about the details of their dataset and files, especially the different file extensions (i.e. .feat)
The Publications Using the Dataset is can be found at the reference below:
References
Andrew L. Maas, Raymond E. Daly, Peter T. Pham, Dan Huang, Andrew Y. Ng, and Christopher Potts. (2011). Learning Word Vectors for Sentiment Analysis. The 49th Annual Meeting of the Association for Computational Linguistics (ACL 2011).

The data will train the data it have, then test it by using the gensim word2vec method. 
It is a word embedding method that will help predict what word could possible be redacted.
The algorithm used from word2vec for this project is its Countinous Bag of Word (CBOW) method.
(THIS METHOD CURRENTLY IS STILL BEING TESTED)
(Files will be updated once the program runs smoothly and tested)

A general discussion of how the word2vec can be used can be found here: 
https://radimrehurek.com/gensim/models/word2vec.html

How to run the python code: 
The framework use for testing the python file: py.test.
Install pytest using the command line: pipenv install pytest

To run the test, on command line type (choose one of the two options): 
pipenv run python -m pytest 
OR
pipenv run python setup.py test