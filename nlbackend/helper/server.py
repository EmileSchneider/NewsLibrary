from flask_restful import Resource, Api
from flask import Flask, request
from flask import jsonify
from flask_cors import CORS

app = Flask(__name__)
api = Api(app)

noundic = {}

def parse(searchString):
    return(searchString.split())

def search(searchString):
    matchlist = []
    p = parse(searchString)
    for word in p:
        matchlist.append(noundic[word])
    return(matchlist)

def xxx():
    l = []
    retdic = {}
    for o in search('Kanzler')[0]:
        l.append(o)


    retdic['nodes'] = [{'id': str(i)} for i in l]
    m = l[:len(l) - 1]
    retdic['links'] = [{'source': str(i) , 'target': str(l[l.index(i) + 1])} for i in m ]
    return(retdic)



class SearchResults(Resource):
    def get(self):
        return jsonify(xxx())

api.add_resource(Flights, '/flights')

CORS(app)

if __name__ == '__main__':
    app.run()