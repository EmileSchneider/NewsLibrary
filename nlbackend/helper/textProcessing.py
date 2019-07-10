import pymongo
import pprint
import nltk
import spacy
import summa

client = pymongo.MongoClient('localhost', 27017)

db = client.items

items = db.scrapy_items
parsed_items = db.parsed_items

word_dict = {}

def addword(word):
    if word in word_dict:
        word_dict[word] = word_dict[word] + 1
    else:
        word_dict[word] = 0

def get_substantivs(text):
    split = text.split()
    retlist = []
    for w in split:
        if w[0].isupper() and len(w) > 3:
            addword(w)
            retlist.append(w)
    return(retlist)

#
# use of spacy and textrank implemantation
#
from rake_nltk import Rake
r = Rake(min_length=1, max_length=1, language='german')
'''
for item in items.find():
    # print(pprint.pprint(item['text']))
    #print(get_substantivs(item['text']))
    #nlp = spacy.load('de_core_news_sm')
    #doc = nlp(item['text'])
    #print(doc.sents)
    r.extract_keywords_from_text(item['text'])
    l = r.get_ranked_phrases()
    doc_dic = {
        "articleID": item['_id'],
        "keyWords": l
    }
    parsed_items.insert_one(doc_dic)
'''

