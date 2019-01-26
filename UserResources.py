
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

class UserRegisterResource(object):

    def __init__(self, pymongo):
        self.db = pymongo

    def on_post(self, req, resp):
        data = req.stream.read(req.content_length or 0)
        user = json.loads(data)

        username = user['username']
        password = user['password']
        location = user['location']

        userQuery = self.db.users.find_one({'username':username})

        if userQuery is not None:
            resp.body = json.dumps({'message': "Username already exists, please enter another"})

        else:
            result = self.db.users.insert_one({'username':username, 'password':password, 'location':location})

            resp.body = json.dumps({'message': "Welcome " + str(username) + '!'})













