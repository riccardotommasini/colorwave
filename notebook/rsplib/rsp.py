import json, os
import requests
from enum import Enum
import datetime, time

import websocket

from websocket import create_connection
    
from rdflib import Graph, ConjunctiveGraph, plugin,URIRef

from IPython.display import display_javascript, display_html, display
import uuid

accessURL = URIRef("http://www.w3.org/ns/dcat#accessURL")
accessURLshort = URIRef("dcat:accessURL")

import pandas as pd

class JSONResult(object):
    def __init__(self, json_data):
        self.uuid = str(uuid.uuid4())
        if isinstance(json_data, dict):
            self.json_str = json.dumps(json_data)
        elif isinstance(json_data, list):
            self.json_str = json.dumps(json_data)
        else:
            self.json_str = json_data
    
    def json(self):
        return json.loads(self.json_str)

    def dataframe(self, numeric=[]):
        data = [b for b in self.json()]
        df = pd.DataFrame.from_dict(data, orient='columns')
        coerce_df_columns_to_numeric(df, numeric)
        return df
    
    def flatten(self):
        return JSONResult([flatten_json(b) for b in self.json()])

    def _ipython_display_(self):
        display_html('<div id="{}" style="height: 150px; width:100%;"></div>'.format(self.uuid),
            raw=True
        )
        display_javascript("""
        require(["https://rawgit.com/caldwell/renderjson/master/renderjson.js"], function() {
          document.getElementById('%s').appendChild(renderjson(%s))
        });
        """ % (self.uuid, self.json_str), raw=True)

class JSONLDResult(JSONResult):
    def __init__(self, json_data):
        if isinstance(json_data, dict):
            self.g = load_graph(json.dumps(json_data))
        elif isinstance(json_data, list):
            self.g = load_graph(json.dumps(json_data))
        elif isinstance(json_data, Graph):
            self.g = json_data
            json_data = self.g.serialize(format='json-ld').decode("utf-8")
        else:
            json_data=json_data
        JSONResult.__init__(self, json_data)

    def rdf(self):
        return self.g
        
    def rdf_table(self):
        return rdf_table(load_graph(self.json_str))
    

default_headers = {
          'Content-Type': 'application/x-www-form-urlencoded',
          'Access-Control-Allow-Origin': '*'
        }

class Endpoint(object):
    def __init__(self, url, method='GET', **kwargs):
        self.method=method
        self.http = "http" in url
        self.url = url;
        self.__dict__.update(kwargs)
    
    def call(self):
        if(self.http):
            return JSONResult(requests.request(self.method, self.url).json())
        else:
            print("Single Connection to WebSocket.")
            ws = create_connection(self.url)
            result =  ws.recv()
            ws.close()
            return JSONLDResult(json.loads(result))

    def __str__(self):
        self.__repr__ ()

    def __repr__(self):
        return self.method + " " + self.url

class Stream(JSONLDResult):
    def __init__(self, url=None, graph=None, res=None):
        if url:
            self.url = url
            r = requests.get(url).json()
            self.g = load_graph(json.dumps(r)) 
        elif graph:
            self.g = graph;
        elif res:
            self.g = res.rdf()
        else:
            raise ValueError('uri or graph')
        JSONLDResult.__init__(self, self.g)
    
    def sgraph(self):
        return self.g
    
    def endpoints(self):
        l1 = [o.value for s,p,o in self.g.triples( (None, accessURLshort, None))] 
        l2 = [o.value for s,p,o in self.g.triples( (None, accessURL, None))]
        return [Endpoint(s) for s in list(set(l1 + l2))] 
    
class RSPService(object):

    def __init__(self, endpoint):
        self.base=endpoint

    def _JSONLDResults(self, res):
        if(res.status_code == requests.codes.ok):
            return JSONLDResult(res.json())
        else:
            return res.text

    def service(self):
        return self._JSONLDResults(requests.get(self.base))

    def streams(self):
        return [Stream(s['iri']) for s in requests.get(self.base + "/streams").json()]
    
    def tasks(self):
        return self._JSONLDResults(requests.get(self.base + "/tasks"))

class RSPPublisher(RSPService):

    def __init__(self, endpoint):
        RSPService.__init__(self, endpoint) 
    
    def lists(self):
        return RSPServices.streams()
        
    def gets(self, qid):
        return self._JSONLDResults(requests.get(self.base + "/streams/" + qid))
                              
    def publish(self, vocals):
        return RSPService._JSONLDResults(requests.post(host+"/streams",  data = json.dumps({'query':vocals}), headers=default_headers))

class RSPEngine(RSPService):
    
    def __init__(self, endpoint):
        RSPService.__init__(self, endpoint) 
    
    def listq(self):
        return self._JSONLDResults(requests.get(self.base + "/queries"))
    
    def tasks(self):
        return self.listq()

    def getq(self, qid):
        return self._JSONLDResults(requests.get(self.base + "/queries/"+qid))
                             
    def create(self, idd, query, tbox, frmt="JSON-LD"):
        body = { 'id':idd, 'tbox': tbox, 'body': query, 'format':frmt}
        return self._JSONLDResults(requests.post(self.base + "/queries", data = json.dumps(body), headers=default_headers))

    def expose(self, qid, protocol='HTTP', retention=3):
        return Stream(res=self._JSONLDResults(requests.post(self.base + "/observers/" + qid, data = json.dumps({'protocol':protocol, "retention":retention}) , headers=default_headers)))
    
    def observers(self, qid):
        print(qid)
        return Stream(res=self._JSONLDResults(requests.get(self.base + "/observers/" + qid)))
    
    def delete(self, qid):
        return self._JSONLDResults(requests.delete(self.base+"/queries/"+qid))

def load_graph(data):
    g = ConjunctiveGraph()
    temp = g.parse(data=data, format='json-ld')
    g.serialize()
    return g

def rdf_table(foo):
    if isinstance(foo, dict):
        g = load_graph(json.dumps(foo))
    elif isinstance(foo, Graph):
        g = foo
    else:
        g = dict(foo)
    
    data = [[t[0],t[1],t[2]] for t in list(g)]
    return pd.DataFrame(data=data, columns=['Subject', 'Predicate', 'Object'])
    
def coerce_df_columns_to_numeric(df, column_list):
    df[column_list] = df[column_list].apply(pd.to_numeric, errors='coerce')
    
def flatten_json(y):
    out = {}

    def flatten(x, name=''):
        if type(x) is dict:
            for a in x:
                flatten(x[a], name + a + '_')
        elif type(x) is list:
            i = 0
            for a in x:
                flatten(a, name + str(i) + '_')
                i += 1
        else:
            out[name[:-1]] = x

    flatten(y)
    return out



