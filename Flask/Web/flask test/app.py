from flask import Flask, render_template, url_for

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')    #öffne html Datei

if __name__  == "__main__":
    app.run(debug=True)


from flask import Flask, render_template, Response
import cv2


app=Flask(__name__)
camera=cv2.VideoCapture(0)


def generate_frames():
    while True:

        success, frame=camera.read() #camera frame lesen
        if not success:
            break
        else:
            ret, buffer=cv2.imencode('.jpg', frame)
            frame=buffer.tobytes()
        yield(b'--frame\r\n'
                b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/video')
def video():
    return Response(generate_frames,mimetype='multipart/x-mixed-replace; boundary=frame')

if __name__ == "__main__":
    app.run(debug=True)




#terminal: .\venv\Scripts\activate
#terminal: flask run
#terminal: "running on" klicken
