import os
from StartingFrame import generate_starting_frame

# Function for Raspberry Pi hosted Flask Server
def get_sensor_data():
    if os.path.exists("current_frame.json"):
        return open("current_frame.json", "r")
    else:
        print("No such File")
        return generate_starting_frame()