from busio import I2C
import numpy as np
import time, board, busio

i2c = busio.I2C(board.SCL, board.SDA, frequency=400000)  # setup I2C


import time, board, busio
import numpy as np
import adafruit_mlx90640
import matplotlib.pyplot as plt
# file in /home/systecs/.local/lib/python3.11/site-packages/adafruit_mlx90640.py

i2c = busio.I2C(board.SCL, board.SDA, frequency=400000)  # setup I2C
mlx = adafruit_mlx90640.MLX90640(i2c)  # begin MLX90640 with I2C comm
mlx.refresh_rate = adafruit_mlx90640.RefreshRate.REFRESH_4_HZ  # set refresh rate

plt.show()

width = 32
height = 24

frame = np.zeros((24 * 32,))  # setup array for storing all 768 temperatures
while True:
    try:
        mlx.getFrame(frame)  # read MLX temperatures into frame var

        # row = []
        # for c in range(width * height):
        #     row.append(frame[c])
        #     if c % width == 0:
        #         print(row)

        print(f"\n\n{frame}\n\n")
        # break
    except ValueError:
        continue  # if error, just read again

# print out the average temperature from the MLX90640
