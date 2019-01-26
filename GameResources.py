import json
import falcon


class CreateGameResource(object):

    def __init__(self, pymongo):
        self.db = pymongo

    def on_post(self, req, resp):
        data = req.stream.read(req.content_length or 0)
        reqJson = json.loads(data)

        # Delete pre-existing games in the database
        self.db.games.delete_many({"username": reqJson["username"]})

        # Create new game
        self.db.games.insert_one({
            "host": reqJson["username"],
            "numPlayers": reqJson["numPlayers"],
            "players": [],
            "initialImages": {},
            "overlayImages": {},
            "guesses": {},
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

        if gameInfo is None:
            resp.body = json.dumps({"message": "Game does not exist"})
        else:
            resp.body = json.dumps(gameInfo)


class RecieveInitialImageResource(object):
    def __init__(self, pymongo):
        self.db = pymongo

    def on_post(self, req, resp):
        data = req.stream.read(req.content_length or 0)
        reqJson = json.loads(data)

        # Find game and return object
        gameInfo = self.db.games.find_one({"host": reqJson["host"]})

        if gameInfo is not None:
            initialImages = gameInfo['initialImages']
            initialImages[reqJson['username']] = reqJson["image"]

            self.db.games.update_one({"host": reqJson["host"]}, {"$set": {"initialImages", initialImages}})
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

            self.db.games.update_one({"host": reqJson["host"]}, {"$set": {"overlayImages", overlayImages}})
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

            self.db.games.update_one({"host": reqJson["host"]}, {"$set": {"guesses", guesses}})
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
            players.append(username)

            self.db.games.update_one({'host': host}, {"$set": {'players': players}})
