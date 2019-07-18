'''
Create the noun dic => dic stored in db

Create the search function => search dic in db

Create returngraph => search db for fitting documents
'''

'''
NLP PIPLINE

1) Raw Text scrape by spider in Mongodb
=> tokenize it
=> remove stopwords 
=> lemmatize words
=> create lexicon (sorted set) of words
*=> create function returns zero vector
*=> create function to update vector given document and function, returns vector
*=> Term Frequency and Inverse Document Frequency IDF = total doc / docs with keyword in
=> store with /raw_text _id/ in db
2) 
relevance ranking
'''

from pymongo import MongoClient
from stop_words import get_stop_words
import nltk

def scrapy_items():
    client = MongoClient()
    db = client.items
    return db.scrapy_items


def removestopwords(artikeltext):
    stop_words = get_stop_words('de')
    punctuation = ['/','.',',',':','!','?',';']
    tokens = nltk.word_tokenize(artikeltext)
    return [token for token in tokens
                if not token in stop_words
                and not token in punctuation]

def makelowercase(tokenlist):
    return [token.lower() for token in tokenlist]

