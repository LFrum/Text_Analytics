# main.py 
# entity-extractor.py

#!/usr/bin/python3
# -*- coding: utf-8 -*-
'''
TRAINING DATA HERE
One of the most important aspects of this project is creating the appropriate set of features. 
Features may include, n-grams in the document, number of letters in the redacted word, 
the number of spaces in the redacted word, etc.
https://www.geeksforgeeks.org/python-word-embedding-using-word2vec/ 
'''
#import redactor
from . import redactor
from . import unredactor

import glob
import io
import os
import pdb
import sys

import nltk
from nltk import sent_tokenize
from nltk import word_tokenize
from nltk import pos_tag
from nltk import ne_chunk
import gensim
from gensim.models import Word2Vec
import warnings

warnings.filterwarnings(action = 'ignore')

def get_entity(text):
    # store all the person names from entity
    names = []
    """Prints the entity inside of the text."""
    for sent in sent_tokenize(text):
        for chunk in ne_chunk(pos_tag(word_tokenize(sent))):
            if hasattr(chunk, 'label') and chunk.label() == 'PERSON':
                #print(chunk.label(), ' '.join(c[0] for c in chunk.leaves()))
                # store the name from chuck leaves                
                name = ' '.join(c[0] for c in chunk.leaves())
                #for leaf in chunk.leaves():
                #    name += leaf[0]
                #    name += " "
                names.append(name)
    # return all the names
    return names

def doextraction(glob_text):
    #print(glob_text)
    glob_text = "'../docs/" + glob_text[1:]
    #print(glob_text)
    data = []
    data_names = []

    """Get all the files from the given glob and pass them to the extractor."""
    for thefile in glob.glob(glob_text):
        with io.open(thefile, 'r', encoding='utf-8') as file:
            text = file.read()
            # replace enter with space
            currText = text.replace("\n", " ")
            data_names = get_entity(text)   

            # iterate through each sentence in the file 
            for i in sent_tokenize(currText): 
                temp = [] 
                
                # tokenize the sentence into words 
                for j in word_tokenize(i): 
                    temp.append(j.lower()) 
            
                data.append(temp) 
  
    # Create CBOW model 
    # size - the dimensionality of the embedding vector
    # window - the number of context words you are looking at
    # min_count - tell the model to ignore words with total count less than this number
    # workers - the number of thread being used
    # sg - wether to use skip-gram = 1 or CBOW = 0
    model1 = gensim.models.Word2Vec(data, min_count = 1000, workers = 4,
                                size = 10000, window = 5, sg = 0) 

if __name__ == '__main__':
    # Usage: python main.py 'train/pos/*.txt'
    trainData = doextraction(sys.argv[-1])

    #redact test data - no need to keep re-doing it
    redactGlob = '../docs/test/pos/*.txt'
    #redactor.doextraction(redactGlob)

    # unredact the test data
    unredactor.predictName(redactGlob,trainData)