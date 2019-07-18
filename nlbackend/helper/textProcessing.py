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
'''
r = Rake(min_length=1, max_length=1, language='german')
item = items.find()[0]
print(item['text'])
r.extract_keywords_from_text(item['text'])
print(nltk.pos_tag(r.get_ranked_phrases()))
def getnoun(word):
    pass
    
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


# Hacky NLP : first get all the nouns from an article and add as keyword to dictionary with a set of the artikle _ids
nlp = spacy.load('de_core_news_sm')

def getnoun(text):
    doc = nlp(text)
    candidate_pos = ['NOUN']
    nouns = []
    for sent in doc.sents:
        for token in sent:
            if token.pos_ in candidate_pos and token.is_stop is False:
                nouns.append(token)

    return(nouns)


noundic = {}

def addnewnouns(nounlist, item_id):
    for n in nounlist:
        n = n.text
        if n in noundic:
            noundic[n].add(item_id)
        else:
            noundic[n] = {item_id}


for item in items.find():
    addnewnouns(getnoun(item['text']), item['_id'])

# Hacky serach functuin

def parse(searchString):
    return(searchString.split())

def search(searchString):
    matchlist = []
    p = parse(searchString)
    for word in p:
        matchlist.append(noundic[word])
    return(matchlist)

def getsecondlevelnodes(objectid):
    secondlevelnodes = []
    for keyword in noundic:
        for obj in noundic[keyword]:
            if objectid['id'] == obj:
                secondlevelnodes.append(objectid['id'])
        print(secondlevelnodes)
    return(secondlevelnodes)

def reactjson(search_string_res):
    retdic = {}
    retdic['nodes'] = []
    retdic['links'] = []

    def getitemheadline(item_id):
        print(items.find(item_id))
        return('someheadline item-id')



    for id in search_string_res[0]:
        retdic['nodes'].append(createnode(id))

    return(retdic)

def createnode(item_id):
    pprint.pprint(type(item_id))
    return({'id' : 'odddd'})

def xxx():
    l = []
    retdic = {}
    for o in search('Kanzler')[0]:
        l.append(o)

    retdic['nodes'] = [{'id': str(i)} for i in l]
    m = l[:len(l) - 1]
    retdic['links'] = [{'source': str(i) , 'target': str(l[l.index(i) + 1])} for i in m ]
    return(retdic)


def yyy(retdic):
    for i in retdic['nodes']:
        print(i)
        print(getsecondlevelnodes(i))
        for j in getsecondlevelnodes(i):
            retdic['nodes'].append({'id' : str(j)})
            retdic['links'].append({'source': i, 'target': str(j)})
    return retdic


from flask import Flask, request
from flask_restful import Resource, Api
from json import dumps
from flask import jsonify
from flask_cors import CORS

app = Flask(__name__)
api = Api(app)


class Flights(Resource):
    def get(self):
        return jsonify(yyy(xxx()))

api.add_resource(Flights, '/flights')

CORS(app)

if __name__ == '__main__':
    app.run()
