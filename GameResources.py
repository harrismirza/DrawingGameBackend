import json
import falcon
from random import choice

catergories = ["alarm_clock",
               "ambulance",
               "angel",
               "ant",
               "backpack",
               "barn",
               "basket",
               "bear",
               "bee",
               "bicycle",
               "bird",
               "book",
               "brain",
               "bridge",
               "bulldozer",
               "bus",
               "butterfly",
               "cactus",
               "calendar",
               "castle",
               "cat",
               "chair",
               "couch",
               "crab",
               "cruise_ship",
               "diving_board",
               "dog",
               "dolphin",
               "duck",
               "elephant",
               "eye",
               "face",
               "fan",
               "fire_hydrant",
               "firetruck",
               "flamingo",
               "flower",
               "frog",
               "garden",
               "hand",
               "hedgehog",
               "helicopter",
               "kangaroo",
               "key",
               "lantern",
               "lighthouse",
               "lion",
               "lobster",
               "map",
               "mermaid",
               "monkey",
               "mosquito",
               "octopus",
               "owl",
               "paintbrush",
               "palm_tree",
               "parrot",
               "passport",
               "peas",
               "penguin",
               "pig",
               "pineapple",
               "pool",
               "postcard",
               "power_outlet",
               "rabbit",
               "radio",
               "rain",
               "rhinoceros",
               "rifle",
               "roller_coaster",
               "sandwich",
               "scorpion",
               "sea_turtle",
               "sheep",
               "skull",
               "snail",
               "snowflake",
               "speedboat",
               "spider",
               "squirrel",
               "steak",
               "stove",
               "strawberry",
               "swan",
               "swing_set",
               "the_mona_lisa",
               "tiger",
               "toothbrush",
               "toothpaste",
               "tractor",
               "trombone",
               "truck",
               "whale",
               "windmill",
               "yoga"]


class CreateGameResource(object):

    def __init__(self, pymongo):
        self.db = pymongo

    def on_post(self, req, resp):
        data = req.stream.read(req.content_length or 0)
        reqJson = json.loads(data)

        # Delete pre-existing games in the database
        self.db.games.delete_many({"host": reqJson["username"]})

        # Create new game
        self.db.games.insert_one({
            "host": reqJson["username"],
            "players": {reqJson["username"]: choice(catergories)},
            "initialImages": {},
            "overlayImages": {},
            "guesses": {},
            "started": False
        })

        resp.body = json.dumps({"message": "Created Game!"})


class GameInfoResource(object):
    def __init__(self, pymongo):
        self.db = pymongo

    def on_post(self, req, resp):
        data = req.stream.read(req.content_length or 0)
        reqJson = json.loads(data)

        # Find game and return object
        gameInfo = self.db.games.find_one({"host": reqJson["host"]})

        del gameInfo["_id"]

        if gameInfo is None:
            resp.body = json.dumps({"message": "Game does not exist"})
        else:
            resp.body = json.dumps(gameInfo)


class ReceiveInitialImagesResource(object):
    def __init__(self, pymongo, tf_runner):
        self.db = pymongo
        self.tfr = tf_runner

    def on_post(self, req, resp):
        data = req.stream.read(req.content_length or 0)
        reqJson = json.loads(data)

        # Find game and return object
        gameInfo = self.db.games.find_one({"host": reqJson["host"]})

        if gameInfo is not None:
            initialImages = gameInfo['initialImages']
            initialImages[reqJson['username']] = reqJson["image"]

            category = gameInfo["players"][reqJson['username']]

            # Trigger ML
            self.tfr.queue.put({
                "host": reqJson["host"],
                "user": reqJson["username"],
                "data": {
                    "category": category,
                    "lines": reqJson["image"]
                }
            })

            self.db.games.update_one({"host": reqJson["host"]}, {"$set": {"initialImages": initialImages}})
            resp.body = json.dumps({"message": "Successfully added image to DB"})
        else:
            resp.body = json.dumps({"message": "Game does not exist"})


class ReceiveOverlayImagesResource(object):
    def __init__(self, pymongo):
        self.db = pymongo

    def on_post(self, req, resp):
        data = req.stream.read(req.content_length or 0)
        reqJson = json.loads(data)

        # Find game and return object
        gameInfo = self.db.games.find_one({"host": reqJson["host"]})

        if gameInfo is not None:
            overlayImages = gameInfo['overlayImages']
            overlayImages[reqJson['username']] = reqJson["images"]

            self.db.games.update_one({"host": reqJson["host"]}, {"$set": {"overlayImages": overlayImages}})
            resp.body = json.dumps({"message": "Successfully added images to DB"})
        else:
            resp.body = json.dumps({"message": "Game does not exist"})


class ReceiveGuessesResource(object):
    def __init__(self, pymongo):
        self.db = pymongo

    def on_post(self, req, resp):
        data = req.stream.read(req.content_length or 0)
        reqJson = json.loads(data)

        # Find game and return object
        gameInfo = self.db.games.find_one({"host": reqJson["host"]})

        if gameInfo is not None:
            guesses = gameInfo['guesses']
            guesses[reqJson['username']] = reqJson["guesses"]

            self.db.games.update_one({"host": reqJson["host"]}, {"$set": {"guesses": guesses}})
            resp.body = json.dumps({"message": "Successfully added guesses to DB"})
        else:
            resp.body = json.dumps({"message": "Game does not exist"})


class JoinGameResource(object):

    def __init__(self, pymongo):
        self.db = pymongo

    def on_post(self, req, resp):
        data = req.stream.read(req.content_length or 0)
        game = json.loads(data)

        host = game['host']
        username = game['username']

        # Find game
        gameQuery = self.db.games.find_one({'host': host})

        if gameQuery is None:
            resp.body = json.dumps({"message": "Unable to find game. Try again or start a new one!"})

        else:
            players = gameQuery['players']
            players[username] = choice(catergories)

            self.db.games.update_one({'host': host}, {"$set": {'players': players}})
            resp.body = json.dumps({"message": str(username) + " joined " + str(host) + "'s game!"})

class StartGameResource(object):
    def __init__(self, pymongo):
        self.db = pymongo

    def on_post(self, req, resp):
        data = req.stream.read(req.content_length or 0)
        game = json.loads(data)

        host = game['host']

        # Find game
        gameQuery = self.db.games.update_one({'host': host}, {"$set":{"started":True}})
