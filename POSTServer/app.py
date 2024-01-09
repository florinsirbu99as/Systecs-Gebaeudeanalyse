from flask import Flask, render_template, Response, url_for, jsonify, request
import cv2, os, json

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


# Video Frame Data Endpoint
@app.route("/data", methods=["POST", "GET"])
def data():
    if request.method == "POST":
        # Handle POST request
        data = request.json
        if "name" in data and "frame_data" in data:
            try:
                with open(
                    "POSTServer/framedata/" + data["name"] + ".json", "w"
                ) as current_frame:
                    current_frame.write(data["frame_data"])
                return "OK", 200
            except IOError as e:
                return f"Error: {e}", 500
    elif request.method == "GET":
        frames_directory = "POSTServer/framedata/"
        frames = []
        for file in os.scandir(frames_directory):
            if file.is_file() and file.name.endswith(".json"):  # Process only JSON files
                try:
                    with open(file.path, "r") as file_content:
                        frame_name = file.name.split('.')[0]
                        frame = {}
                        frame["name"] = frame_name
                        frame["frame_data"] = json.loads(file_content.read())
                        frames.append(frame)
                except Exception as e:
                    frames[file.name] = f"Error reading file: {str(e)}"
        return frames, 200


if __name__ == "__main__":
    app.run(host="0.0.0.0", debug=True)
