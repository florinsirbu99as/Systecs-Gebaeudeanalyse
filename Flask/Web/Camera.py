from busio import I2C
import numpy as np
from flask import jsonify
from time import sleep
from StartingFrame import generate_starting_frame

import json, adafruit_mlx90640, os, board, busio


def start_camera():
    i2c = busio.I2C(board.SCL, board.SDA, frequency=400000)
    mlx = adafruit_mlx90640.MLX90640(i2c)
    mlx.refresh_rate = adafruit_mlx90640.RefreshRate.REFRESH_4_HZ

    frame = np.zeros((24 * 32,))

    while True:
        try:
            mlx.getFrame(frame)
            # Convert frame to JSON and return it
            with open("current_frame.json", "w") as current_frame:
                current_frame.write(json.dumps(frame.tolist()))
            # return json.dumps(frame.tolist())
            print("written")
        except Exception:
            continue

start_camera()