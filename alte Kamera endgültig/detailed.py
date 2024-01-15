
# Libraries
import os
import math
import time
import sys

import numpy as np
import pygame
import busio
import board

from scipy.interpolate import griddata

from colour import Color

import adafruit_amg88xx

# Set up I2C communication with the AMG8833 sensor
i2c_bus = busio.I2C(board.SCL, board.SDA)

# Define temperature range constants (min, max)
MINTEMP = 26.0
MAXTEMP = 32.0

# Define the color depth for temperature mapping
COLORDEPTH = 1024

# Set the SDL framebuffer device
os.putenv("SDL_FBDEV", "/dev/fb1")

# Initialize the pygame library
pygame.init()

# Initialize the AMG8833 sensor
sensor = adafruit_amg88xx.AMG88XX(i2c_bus)

# Create a grid of points for temperature interpolation
points = [(math.floor(ix / 8), (ix % 8)) for ix in range(0, 64)]
grid_x, grid_y = np.mgrid[0:7:32j, 0:7:32j]

# Set up the display dimensions and initialize colors
height = 240
width = 240

blue = Color("indigo")
colors = list(blue.range_to(Color("red"), COLORDEPTH))
colors = [(int(c.red * 255), int(c.green * 255), int(c.blue * 255)) for c in colors]

# Set up display pixel dimensions and initialize the LCD screen
displayPixelWidth = width / 30
displayPixelHeight = height / 30
lcd = pygame.display.set_mode((width, height))
lcd.fill((255, 0, 0))
pygame.display.update()
pygame.mouse.set_visible(False)
lcd.fill((0, 0, 0))
pygame.display.update()

# Define utility functions for value mapping
def constrain(val, min_val, max_val):
    return min(max_val, max(min_val, val))

def map_value(x, in_min, in_max, out_min, out_max):
    return (x - in_min) * (out_max - out_min) / (in_max - in_min) + out_min

# Allow some time for the sensor to stabilize
time.sleep(0.1)

# Continuous loop for reading sensor data and updating display
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    try:                                                                                                # Read temperature values from the sensor pixels
        pixels = []
        for row in sensor.pixels:
            pixels = pixels + row
        pixels = [map_value(p, MINTEMP, MAXTEMP, 0, COLORDEPTH - 1) for p in pixels]                     # Map temperature values to color intensity
        bicubic = griddata(points, pixels, (grid_x, grid_y), method="cubic")                            # Perform bicubic interpolation for smoother temperature mapping

        # Update the display with temperature-mapped colors
        for ix, row in enumerate(bicubic):
            for jx, pixel in enumerate(row):
                pygame.draw.rect(
                    lcd,
                    colors[constrain(int(pixel), 0, COLORDEPTH - 1)],
                    (
                        displayPixelHeight * ix,
                        displayPixelWidth * jx,
                        displayPixelHeight,
                        displayPixelWidth,
                    ),
                )
        pygame.display.update()
    except OSError as errObject:
        # Handle OSError, such as I2C communication errors
        print(errObject.strerror)
