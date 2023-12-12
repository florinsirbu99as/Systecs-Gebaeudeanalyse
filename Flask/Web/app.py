from flask import Flask, render_template, Response
from CameraFunctions import get_sensor_data
from StartingFrame import generate_starting_frame

import cv2

app = Flask(__name__)


def generate_frames():
    cap = cv2.VideoCapture(0)  # Change this to your screen capture device index

    while True:
        success, frame = cap.read()
        if not success:
            break
        else:
            _, buffer = cv2.imencode(".jpg", frame)
            frame = buffer.tobytes()
            yield (b"--frame\r\n" b"Content-Type: image/jpeg\r\n\r\n" + frame + b"\r\n")

    cap.release()


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/streaming")
def streaming():
    temperature_data = generate_starting_frame()
    return render_template("streaming.html", temperature_data=temperature_data)


@app.route("/video_feed")
def video_feed():
    return Response(
        generate_frames(), mimetype="multipart/x-mixed-replace; boundary=frame"
    )


@app.route("/get_data")
def get_data():
    return get_sensor_data()


if __name__ == "__main__":
    app.run(host="0.0.0.0", debug=True)
