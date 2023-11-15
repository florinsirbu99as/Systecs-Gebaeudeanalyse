import os

# default path for this file on Raspbian
dir = "/boot/config.txt"
dir = "C:/temp/test.txt"
status = ""

# Check if File exists
if os.path.exists(dir):
    status = "File exists."
    # first read(r) then update(+) File
    with open(dir, mode="r+") as file:
        status = "File opened."
        lines = file.readlines()
        for lineIndex in range(len(lines)):
            line = lines[lineIndex]
            if line.find("dtparam=i2c_arm=on") > -1:
                status = "Line exists."
                lines[lineIndex] = "dtparam=i2c_arm=on, i2c_arm_baudrate=400000"
                break
        if status == "Line exists.":
            file.seek(0)
            file.truncate()
            file.writelines(lines)
            status = "Baudrate written."
else:
    status = "File does not exist."

print(status)
