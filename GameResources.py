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
            "initialImages": [[]*reqJson["numPlayers"]],
            "overlayImages": [[] * reqJson["numPlayers"]],
            "guesses": [[] * reqJson["numPlayers"]]
        })

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







