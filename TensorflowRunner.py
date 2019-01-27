import multiprocessing
import json
import requests
from pymongo import MongoClient
import traceback


class TensorflowRunner(object):

    def __init__(self):
        self.queue = multiprocessing.Queue()
        self.p = multiprocessing.Process(target=self.startProcessing)
        self.p.start()

    def startProcessing(self):
        while True:
            try:
                job = self.queue.get()
                print("Got job!")

                # Send job to NodeJS Server
                url = "http://localhost:3005/"
                response = requests.post(url, json=job["data"])

                lines = response.json()
                print("Received response")

                # Save lines to database in appropriate place
                db = MongoClient('localhost', 27017).draw

                # Get current game
                game = db.games.find_one({"host": job["host"]})
                overlayImages = game["overlayImages"]
                overlayImages["AI"] = {}
                overlayImages["AI"][job["user"]] = lines

                db.games.update_one({"host": job["host"]}, {"$set": {"overlayImages": overlayImages}})
            except:
                traceback.print_exc()
                pass
