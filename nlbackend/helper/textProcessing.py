import pymongo
import pprint
client = pymongo.MongoClient('localhost', 27017)

db = client.items

items = db.scrapy_items

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

for item in items.find():
    # print(pprint.pprint(item['text']))
    print(get_substantivs(item['text']))