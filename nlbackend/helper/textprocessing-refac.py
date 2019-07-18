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


def makelexicon(lex):
    return MongoClient.items.nlp.lexicon.insert(lex)


def savelexicon(lex):
    return MongoClient.items.nlp.lexicon.save(lex)


def getlexicon():
    return MongoClient.items.nlp.lexicon.find_one()


def updatelexicon(lex, tokenlist):
    for t in tokenlist:
        if t not in lex:
            lex[t] = 0
        if t in lex:
            lex[t] = lex[t] + 1
    return lex


class NewsItemProcessingFactory():
    def __init__(self):
        client = MongoClient()
        db = client.items
        rawitems = self.__connectDBrawitems__()
        processeditems = self.__connectDBprocesseditems__()

    def __connectDBprocesseditems__(self):
        return self.db.processed_items

    def __connectDBrawitems__(self):
        return self.db.scrapy_items

    def getunprocesseditems(self):
        pass

    def processitem(self):
        pass

