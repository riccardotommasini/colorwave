import json, os
import requests
from enum import Enum
import datetime, time

from IPython.display import display_javascript, display_html, display
import uuid

class RenderJSON(object):
    def __init__(self, json_data):
        if isinstance(json_data, dict):
            self.json_str = json.dumps(json_data)
        elif isinstance(json_data, list):
            self.json_str = json.dumps(json_data)
        else:
            self.json_str = json
        self.uuid = str(uuid.uuid4())
        
    def _ipython_display_(self):
        display_html('<div id="{}" style="height: 150px; width:100%;"></div>'.format(self.uuid),
            raw=True
        )
        display_javascript("""
        require(["https://rawgit.com/caldwell/renderjson/master/renderjson.js"], function() {
          document.getElementById('%s').appendChild(renderjson(%s))
        });
        """ % (self.uuid, self.json_str), raw=True)

default_headers = {
          'Content-Type': 'application/x-www-form-urlencoded',
          'Access-Control-Allow-Origin': '*'
        }

class RSPService(object):

    def __init__(self, endpoint):
        self.base=endpoint

    def _results(self, res):
        if(res.status_code == requests.codes.ok):
            return RenderJSON(res.json())
        else:
            return res.text

    def service(self):
        return self._results(requests.get(self.base))

    def streams(self):
        return self._results(requests.get(self.base + "/streams"))


class RSPPublisher(RSPService):

    def __init__(self, endpoint):
        RSPService.__init__(self, endpoint) 
        
    def publish(self, vocals):
        return RSPService._results(requests.post(host+"/streams",  data = json.dumps({'query':vocals}), headers=default_headers))

class RSPEngine(RSPService):
    
    def __init__(self, endpoint):
        RSPService.__init__(self, endpoint) 

    def queries(self):
        return self._results(requests.get(self.base + "/queries"))

    def query(self, idd, query, tbox, frmt="JSON-LD"):
        body = { 'id':idd, 'tbox': tbox, 'body': query, 'format':frmt}
        return self._results(requests.post(self.base + "/queries", data = json.dumps(body), headers=default_headers))

    def observer(self, qid, protocol='HTTP', retention=3):
        return self._results(requests.post(self.base + "/" + qid, data = json.dumps({'protocol':protocol, "retention":retention}) , headers=default_headers))




