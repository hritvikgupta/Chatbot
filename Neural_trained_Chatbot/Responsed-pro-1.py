# -*- coding: utf-8 -*-
"""
Created on Wed Jul 15 09:19:07 2020

@author: hritvikgupta
"""
import pandas as pd
import numpy as np
import string
import nltk
import tensorflow as tf
import keras
import sklearn
import re
import sys
import string
import os
import scipy
import random

##Audio
import speech_recognition as sr
import pyaudio
import IPython

#Model
from keras.preprocessing.text import Tokenizer
from sklearn.feature_extraction.text import TfidfVectorizer
from keras.preprocessing.sequence import pad_sequences
from keras.layers import LSTM, Dense, Embedding, Dropout
from tensorflow.keras import utils
from sklearn.metrics.pairwise import cosine_similarity
from ast import literal_eval 
  


nltk.download('stopwords')
nltk.download("punkt")
nltk.download('wordnet')
stopwords = nltk.corpus.stopwords.words("english")


##Importing the files
high_school_input = pd.read_csv("C:\\Users\hritvik gupta\Desktop\high.csv", delimiter = '\t', encoding = 'utf-8')
elementry = pd.read_csv("C:\\Users\hritvik gupta\Desktop\elementry.csv", delimiter = '\t', encoding = 'utf-8')
def convert(lst): 
    return literal_eval(lst) 

elementry['Subject']  = elementry['Subject'].apply(lambda x : convert(x))
elementry['Concepts'] = elementry['Concepts'].apply(lambda x : convert(x))

elem_list_new = ''
for i in range(len(elem_list)):
    for j in range(len(elem_list[i])):
        elem_list_new += elem_list[i][j]
    elem_list_new += '\n'+'END'
    
v = elementry.assign(Subject=elementry.Subject).explode('Subject')
v = v.drop('Concepts', axis=1)
elem_list = v.values.tolist()
elem_list[0]

def Convert(string): 
    li = list(string.split("\n")) 
    return li 

z = Convert(elem_list_new)
z[0]

GREETING_INPUTS = ('hello','hi', 'greetings', 'sup', "what's up", 'hey')
GREETING_RESPONSES = ['hi', 'hey','"nods"', 'hi there', 'hello','I am glad you are talking to me']

def greeting(sentence):
  for word in sentence.split():
    if word.lower() in GREETING_INPUTS:
      return random.choice(GREETING_RESPONSES)
  
def clean_text(text):
    text = " ".join([w.lower() for w in text ])
p = z
def response(user_response):
    robo_response=''
    z.append(user_response)  
    TfidfVec = TfidfVectorizer()
    tfidf = TfidfVec.fit_transform(z)
    vals = cosine_similarity(tfidf[-1], tfidf)
    idx=vals.argsort()[0][-2]
    flat = vals.flatten()
    flat.sort()
    req_tfidf = flat[-2]  
    if(req_tfidf==0):
        robo_response=robo_response+"I am sorry! I don't understand you"
        return robo_response
    else:
        robo_response = robo_response+z[idx]+z[idx-1]+z[idx+1]
        return robo_response

    
flag = True
print("Robo my name is robo i will answr your queries about chatbots if you wnat to exit type bye")
while flag==True:
  user_response = input("How may I Help You.....")
  user_response = user_response.lower()
  if user_response != 'bye':
    if user_response=='thanks' or user_response == 'thank you':
      flag = False
      print('Robo: you are welcome')
    else:
      if (greeting(user_response) != None):
        print("ROBO: "+greeting(user_response))  
      else:
        print("ROBO:", end= "")  
        if "reccomendation" in user_response or "reccomend" in user_response:
            print('which std. Elementry or the High school')
            ques = input("Respond")
            if ques == 'elementry':
                ques2 = input("Which course you are looking for...")
                l = response(ques2)
                for i in l.split("END"):
                    print(i)
                    print("\n")
                z.remove(ques2)
  else:
    flag = False
    print("ROBO: BYE Take Care: ")
    
z.remove('landform')


#!pip install dialogflow
#import dialogflow_v2beta1
