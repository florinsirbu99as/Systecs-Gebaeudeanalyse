from flask import Flask, render_template, Response, url_for, jsonify, request
import cv2
import requests
#from CameraFunctions import get_sensor_data
from StartingFrame import generate_starting_frame

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

# @app.route("/get_data")
# def get_data():
#     return get_sensor_data()

# POST endpoint
@app.route('/post_data', methods=['POST'])
def post_data():
    # Get data from the POST request
    data = request.json  # Assuming JSON data is sent in the POST request
    # Process the data or perform actions based on the POST request
    temperature_data = data
    with open('POSTServer/static/current_frame.json','w') as current_frame:
        current_frame.write(data)

    # Return a response
    return jsonify({'message': f'Received value: {data}'}), 200  # Send back a JSON response

@app.route('/get_current_frame')
def get_current_frame():
    return open('POSTServer/static/current_frame.json','r') 

if __name__ == '__main__':
    app.run(debug=True)

if __name__ == "__main__":
    app.run(host="0.0.0.0", debug=True)
