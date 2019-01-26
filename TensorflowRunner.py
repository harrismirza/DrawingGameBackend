import multiprocessing
import tensorflow
import json
import numpy as np


class TensorflowRunner(object):

    def __init__(self):
        self.queue = multiprocessing.Queue()

    def startProcessing(self):
        while True:
            job = self.queue.get()

            # Load model


if __name__ == '__main__':
    # Test Loading model
    modelPath = "./nodejs code/alarm_clock.gen.full.json"
    modelData = json.load(open("./nodejs code/alarm_clock.gen.full.json", "r"))
    info = modelData[0]
    dimensions = modelData[1]
    num_blobs = dimensions.length
    weightsIn = modelData[2]
    weights = [0] * len(weightsIn)
    max_weight = 10.0
    N_mixture = 20

    max_seq_len = info.max_seq_len

    pixel_factor = 2.0
    scale_factor = info.scale_factor / pixel_factor

    for i in range(0, num_blobs):
        weights[i] = np.Array(weightsIn[i])
