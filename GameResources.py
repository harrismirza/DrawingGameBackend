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
        self.db.games.write_one({
            "host": reqJson["username"],
            "numPlayers": reqJson["numPlayers"],
            "players": [],
            "initialImages": [[]*reqJson["numPlayers"]],
            "overlayImages": [[] * reqJson["numPlayers"]],
            "guesses": [[] * reqJson["numPlayers"]]
        })

