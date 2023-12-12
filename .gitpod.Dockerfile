FROM gitpod/workspace-full

# Install OpenCV dependencies
RUN sudo apt-get update && \
    sudo apt-get install -y libsm6 libxext6 libxrender-dev

# Install OpenCV
RUN pip install opencv-python-headless

# Install Xvfb
RUN sudo apt-get install -y xvfb

# Set display
ENV DISPLAY=:99

# RUN apt-get update && apt-get install libgl1

# RUN apt-get update && apt-get install ffmpeg libsm6 libxext6  -y