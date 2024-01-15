
import time, sys
sys.path.append('../')
# Import the AMG8833 module for interfacing with the sensor
import amg8833_i2c
import numpy as np
import matplotlib.pyplot as plt

# Measure time for sensor initialization
t0 = time.time()
sensor = []

# Wait 1 second for the sensor to start
while (time.time() - t0) < 1:
    try:
        # Try initializing AMG8833 with AD0 = 5V and address 0x69
        sensor = amg8833_i2c.AMG8833(addr=0x69)
    except:
        # If unsuccessful, try initializing with AD0 = GND and address 0x68
        sensor = amg8833_i2c.AMG8833(addr=0x68)
    finally:
        pass

# Wait for the sensor to settle
time.sleep(0.1)

# Exit the script if the sensor is not found
if sensor == []:
    print("No AMG8833 Found - Check Your Wiring")
    sys.exit()



# Set font size for the plot
plt.rcParams.update({'font.size': 16})

# Define figure dimensions
fig_dims = (12, 9)

# Initialize the figure
fig, ax = plt.subplots(figsize=fig_dims)

# Set pixel resolution and create an array of zeros
pix_res = (8, 8)
zz = np.zeros(pix_res)

# Plot initial image with temperature bounds
im1 = ax.imshow(zz, vmin=15, vmax=40)

# Create and format the colorbar
cbar = fig.colorbar(im1, fraction=0.0475, pad=0.03)
cbar.set_label('Temperature [C]', labelpad=10)

# Draw the figure
fig.canvas.draw()

# Create a background copy for speeding up runs
ax_bgnd = fig.canvas.copy_from_bbox(ax.bbox)

# Show the figure
fig.show()

# Specify the number of pixels to read
pix_to_read = 64

# Continuous loop for reading and plotting sensor data
while True:
    # Read temperature values from the sensor pixels with status
    status, pixels = sensor.read_temp(pix_to_read)

    # If there's an error in pixel reading, re-enter the loop and try again
    if status:
        continue

    # Read thermistor temperature
    T_thermistor = sensor.read_thermistor()

    # Restore the background for faster plotting
    fig.canvas.restore_region(ax_bgnd)

    # Update the plot with new temperature data
    im1.set_data(np.reshape(pixels, pix_res))

    # Draw the image again
    ax.draw_artist(im1)

    # Blit the figure for speeding up the run
    fig.canvas.blit(ax.bbox)

    # Flush events for real-time plotting
    fig.canvas.flush_events()

    # Print the thermistor temperature
    print("Thermistor Temperature: {0:2.2f}".format(T_thermistor))
