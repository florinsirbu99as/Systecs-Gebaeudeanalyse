from busio import I2C
import numpy as np
import time, board, busio
from flask import jsonify


import time, board, busio
import numpy as np
import adafruit_mlx90640

# file in /home/systecs/.local/lib/python3.11/site-packages/adafruit_mlx90640.py


def get_sensor_data():
    i2c = busio.I2C(board.SCL, board.SDA, frequency=400000)
    mlx = adafruit_mlx90640.MLX90640(i2c)
    mlx.refresh_rate = adafruit_mlx90640.RefreshRate.REFRESH_4_HZ

    frame = np.zeros((24 * 32,))

    while(True):
        try:
            mlx.getFrame(frame)
            # You can manipulate 'frame' here if needed before returning
            return jsonify(
                sensor_data=frame.tolist()
            )  # Convert frame to JSON and return it
        except Exception:
            continue
