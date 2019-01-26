
import json
import falcon

class UserLoginResource(object):

    def __init__(self, pymongo):
        self.db = pymongo

    def on_post(self, req, resp):
        data = req.stream.read(req.content_length or 0)
        user = json.loads(data)

        username = user['username']
        password = user['password']

        userQuery = self.db.users.find_one({'username':username, 'password':password})

        if userQuery is None:
            resp.body = json.dumps({'auth': False})

        else:
            resp.body = json.dumps({'auth': True, 'location': userQuery['location']})














