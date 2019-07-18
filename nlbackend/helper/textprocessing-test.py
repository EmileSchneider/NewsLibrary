import importlib


def test_getitem():
    'getitem returns a dic from the db by id'
    id = '5d1f330599f952de3c51746d'
    assert getitem(id)['_id'] == id

def test_tokenizer():
    string = "Die Welt heutzutage, nach ein unangenehmes erwachen, ist verloren."
    assert tokenize(string) == ['Die', 'Welt', 'heutzutage', 'nach', 'ein', 'unangenehmes',
                               'erwachen', 'ist', 'verloren' ]
def test_removestopwords():
    tokens = ['Die', 'Welt', 'heutzutage', 'nach', 'ein', 'unangenehmes',
                               'erwachen', 'ist', 'verloren' ]
    assert removestopwords(tokens) == ['Welt', 'heutzutage', 'unangenehmes', 'erwachen', 'verloren']

def test_lemmative():
    tokens = ['Welt', 'heutzutage', 'unangenehmes', 'erwachen', 'verloren']

from pymongo import MongoClient
client = MongoClient()
db = client.items
items = db.scrapy_items
import sys

def getitem(id):
    try:
        items.find_one(id)
    except:
        sys.exc_info()[0]
