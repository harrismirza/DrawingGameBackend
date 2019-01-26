import falcon
import waitress
from pymongo import MongoClient

from HelloWorldResources import HelloWorldResource
from UserResources import UserLoginResource, UserRegisterResource

if __name__ == '__main__':
    api = falcon.API()
    pymongo = MongoClient('localhost', 27017)
    api.add_route("/hello", HelloWorldResource(pymongo.draw))
    api.add_route("/user/login", UserLoginResource(pymongo.draw))
    api.add_route("/user/register", UserRegisterResource(pymongo.draw))

    print("Created API")

    waitress.serve(api, host='127.0.0.1', port=5555)
