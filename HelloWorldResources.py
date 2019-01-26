import json

import falcon


class HelloWorldResource(object):

    def __init__(self, pymongo):
        self.pymongo = pymongo

    def on_get(self, req, resp):
        resp.body = json.dumps({"response": "Hello, World!"})
        resp.status = "200"