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
import pprint
import copy
import re
from collections import OrderedDict
def scrapy_items():
    client = MongoClient()
    db = client.items
    return db.scrapy_items


def removestopwords(artikeltext):
    stop_words = get_stop_words('de')
    punctuation = ['/','.',',',':','!','?',';']
    tokens = nltk.word_tokenize(artikeltext)
    tokens = makelowercase(tokens)
    return [token for token in tokens
                if not token in stop_words
                and not token in punctuation]


def makelowercase(tokenlist):
    return [token.lower() for token in tokenlist]


def makelexicon(lex):
    return MongoClient().items.nlp.lexicon.insert_one(lex)


def savelexicon(lex):
    return MongoClient().items.nlp.lexicon.insert_one(lex)


def getlexicon():
    return MongoClient().items.nlp.lexicon.find_one()


def updatelexicon(lex, tokenlist):
    for t in tokenlist:
        if re.search("^[a-zA-Z]+$", t):
            if t not in lex:
                lex[t] = 0
            if t in lex:
                lex[t] = lex[t] + 1
    return lex


class NewsItemProcessingFactory():
   def __init__(self):
       self.lexicon = getlexicon()
       self.rawitems = MongoClient().items.scrapy_items
       self.parseditems = MongoClient().items.parsed_items
       self.lexicon = MongoClient().items.lexicon
       self.tfidfvectors = MongoClient().items.tfidfvectors
       self.zero_vec = []

   def processrawitems(self):
       for doc in self.rawitems.find({}, {'parsed': False}):
           self.parseditems.insert_one({'real-id': doc['_id'],
                                        'artikel-text': removestopwords(doc['text'])})
           self.rawitems.update_one({'_id': doc['_id']}, {'$set' : {'parsed': True}})

   def updatelexicon(self):
       lex = {}
       for doc in self.parseditems.find({}):
           lex = updatelexicon(lex, doc['artikel-text'])
       self.lexicon.insert_one(lex)

   def lexicon2zerovec(self):
       zero_vec = OrderedDict((token, 0) for token in self.lexicon.find_one({}))
       return zero_vec

   def counttoken(self, tokens, token):
       c = 0
       for t in tokens:
           if t == token:
               c = c + 1
       return c

   def docvectors(self):
       v = self.lexicon2zerovec()
       l = len(v)
       veclist = []
       for doc in self.parseditems.find({}):
           vec = copy.copy(v)
           tokens = doc['artikel-text']
           for t in tokens:
               term_frequency = self.counttoken(tokens, t) / len(tokens)
               other_doc_with_keyword = 0
               for d in self.parseditems.find({}):
                   if t in d['artikel-text']:
                       other_doc_with_keyword = other_doc_with_keyword + 1
               inverse_doc_frequency = len(list(self.parseditems.find())) / other_doc_with_keyword
               vec[t] = term_frequency * inverse_doc_frequency
           pprint.pprint(vec)
           veclist.append(vec)
       return veclist