FROM gitpod/workspace-full

# Install OpenCV dependencies
RUN sudo apt-get update && \
    sudo apt-get install -y libsm6 libxext6 libxrender-dev

# Install OpenCV
RUN pip install opencv-python-headless