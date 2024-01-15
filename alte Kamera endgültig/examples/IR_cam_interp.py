
# Libraries
import time
import sys
sys.path.append('../')  # Add the parent directory to the system path

import amg8833_i2c
import numpy as np
import matplotlib.pyplot as plt
from scipy import interpolate

# Initialize a timer to run the sensor initialization for a short duration
t0 = time.time()
sensor = []
while (time.time() - t0) < 1:
    try:
        # Attempt to initialize the AMG8833 sensor with a specific I2C address
        sensor = amg8833_i2c.AMG8833(addr=0x69)
    except:
        # If the first address fails, attempt to initialize with an alternate address
        sensor = amg8833_i2c.AMG8833(addr=0x68)
    finally:
        pass
time.sleep(0.1)


# Check if the sensor is not found, print a message, and exit the application
if sensor == []:
    print("No AMG8833 Found - Check Your Wiring")
    sys.exit()


# Set up the pixel resolution and create grids for interpolation
pix_res = (8, 8)
xx, yy = (np.linspace(0, pix_res[0], pix_res[0]),
          np.linspace(0, pix_res[1], pix_res[1]))
zz = np.zeros(pix_res)


# Set up interpolation parameters
pix_mult = 6
interp_res = (int(pix_mult * pix_res[0]), int(pix_mult * pix_res[1]))
grid_x, grid_y = (np.linspace(0, pix_res[0], interp_res[0]),
                  np.linspace(0, pix_res[1], interp_res[1]))


# Define a function for 2D interpolation
def interp(z_var):
    f = interpolate.interp2d(xx, yy, z_var, kind='cubic')
    return f(grid_x, grid_y)


# Interpolate the zero-initialized grid
grid_z = interp(zz)


# Set up the plot with specified figure dimensions
plt.rcParams.update({'font.size': 16})
fig_dims = (10, 9)
fig, ax = plt.subplots(figsize=fig_dims)
fig.canvas.set_window_title('AMG8833 Image Interpolation')


# Display the initial interpolated grid
im1 = ax.imshow(grid_z, vmin=18, vmax=37, cmap=plt.cm.RdBu_r)
cbar = fig.colorbar(im1, fraction=0.0475, pad=0.03)
cbar.set_label('Temperature [C]', labelpad=10)
fig.canvas.draw()


# Copy the background for efficient updating
ax_bgnd = fig.canvas.copy_from_bbox(ax.bbox)
fig.show()


# Specify the number of pixels to read
pix_to_read = 64
while True:
    # Read temperature values from the sensor pixels
    status, pixels = sensor.read_temp(pix_to_read)
    if status:
        continue

    # Read thermistor temperature
    T_thermistor = sensor.read_thermistor()

    # Restore the background and update the plot with new temperature data
    fig.canvas.restore_region(ax_bgnd)
    new_z = interp(np.reshape(pixels, pix_res))
    im1.set_data(new_z)
    ax.draw_artist(im1)
    fig.canvas.blit(ax.bbox)
    fig.canvas.flush_events()
