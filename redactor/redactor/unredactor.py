# unredactor.py
# -*- coding: utf-8 -*-
from . import redactor
from . import main

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
from scipy import spatial
from operator import itemgetter
import time
import multiprocessing        
               
def predictName(glob_text, trainData):
    #currOutputName = ""    
    outputFolder = "/prediction/"
    if os.path.isdir(outputFolder) == False:
        os.mkdir(outputFolder)
    
    for thefile in glob.glob(glob_text):
        currOutputName = thefile.replace(".txt", ".predicted.txt")
        currOutputName = outputFolder + currOutputName
        currOutput = open(currOutputName, "w", encoding='utf-8')
        
        with io.open(thefile,'r',encoding="utf-8") as file:
            text = file.read()
            redacted_feature = redactedFeature (text)
            file.close()
            td = trainData
            fd = redacted_feature
            sim_fd = []
            count = 0
            for i in fd:
                vec = []
                count += 1
                vec.append(count)
                sim = []
                x = []
                #print("length of train data: ", td)
                currOutput.write("length of train data: %s" % td)
                for j in td:
                    temp = []
                    temp.append(j[0])
                    temp.append(cos_similar(i,j[1]))
                    sim.append(temp)
                    sim=sorted(sim,key=itemgetter(1),reverse=True)
                for i in range(0,3):
                    #print("sim[i]",sim[i])
                    currOutput.write("sim[i]: %s" % sim[i])
                    x.append(sim[i])
                vec.append(x)
                sim_fd.append(vec)
        for i in sim_fd:
            print("The top three most likely word for the {0} redacted word in file are: {1}\n".format(i[0],i[1]), file=currOutput)
        if len(sim_fd) == 0:
            print("There are no person names in the file!!", file=currOutput)

    currOutput.close()
    #print("predictName: DONE") 

def redactedFeature (text):
    #print("get_feature_redacted: START")
    feature = []
    w = 0            
    w = len(nltk.word_tokenize(text))
    count = 0
    space = 0
    count_word = 0
    count_Redacted = 0   
    l=[]
    for i in range(0,len(text)):
        if text[i] == u"\u2588":
            count_word=1
            count+=1
        else:
            if (text[i-1] == u"\u2588" and text[i+1] == u"\u2588"):
                #i=i+1
                space += 1
                continue
            if (count > 0):
                if space >= 0:
                    l.append(space)
                l.append(count)
                l.append(w)
                feature.append(l)
                l=[]
            count = 0     
            space = 0
            if count_word == 1:
                count_Redacted += 1
                count_word = 0
    feature_actual=[]
    for i in feature:
        l = []
        l.append(count_Redacted)
        for j in i:
            l.append(j)
        feature_actual.append(l)
    return feature_actual       

def cos_similar(v1,v2):
    result = 1 - spatial.distance.cosine(v1, v2)
    return result       