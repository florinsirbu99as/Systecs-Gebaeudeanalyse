import os

dir = "/boot/config.txt"
status = ""
if os.path.exists(dir):
    status = "File exists."
    with open(dir) as file:
        for lineIndex in range(file.readlines):
            line = file.readlines[lineIndex]
            if line == "dtparam=i2c_arm=on":
                status = "Line exists."
                file.readlines[lineIndex] = "dtparam=i2c_arm=on, i2c_arm_baudrate=400000"
                status = "Line written."
                break
else:
    status = "File does not exist."

print(status)