from busio import I2C
import numpy as np
import time, board, busio
from flask import jsonify
from time import sleep

import json
import adafruit_mlx90640
import requests


# Function for external hosted Server
def Post_Data():
    i2c = busio.I2C(board.SCL, board.SDA, frequency=400000)
    mlx = adafruit_mlx90640.MLX90640(i2c)
    mlx.refresh_rate = adafruit_mlx90640.RefreshRate.REFRESH_4_HZ

    frame = np.zeros((24 * 32,))

    try:
        mlx.getFrame(frame)
        url = "https://5000-florinsirbu-systecsgeba-gksmt1k8cfn.ws-eu107.gitpod.io/data"
        postRequest = requests.post(
            url, json={"name": "Raspberry 1", "frame": frame.tolist()}
        )
        if postRequest.status_code != 200:
            print(postRequest.status_code, "Not Ok")
        else:
            print("OK")
    except Exception as ex:
        print("ERROR: Failed to get Frame\n", ex)


while True:
    Post_Data()
