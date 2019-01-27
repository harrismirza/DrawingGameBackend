import falcon
import waitress
from pymongo import MongoClient

from UserResources import *
from GameResources import *
from TensorflowRunner import TensorflowRunner

if __name__ == '__main__':
    api = falcon.API()

    # Create Mongo
    pymongo = MongoClient('localhost', 27017)

    # Create TF Queue
    tfr = TensorflowRunner()

    api.add_route("/user/login", UserLoginResource(pymongo.draw))
    api.add_route("/user/register", UserRegisterResource(pymongo.draw))
    api.add_route("/game/create", CreateGameResource(pymongo.draw))
    api.add_route("/game/join", JoinGameResource(pymongo.draw))
    api.add_route("/game/info", GameInfoResource(pymongo.draw))
    api.add_route("/game/initial_images", ReceiveInitialImagesResource(pymongo.draw, tfr))
    api.add_route("/game/overlay_images", ReceiveOverlayImagesResource(pymongo.draw))
    api.add_route("/game/guesses", ReceiveGuessesResource(pymongo.draw))

    print("Created API")

    waitress.serve(api, host='127.0.0.1', port=5555)
