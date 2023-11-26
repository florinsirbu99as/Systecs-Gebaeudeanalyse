from flask import Flask, render_template

app = Flask(__name__)

@app.route('/')
def index():
    # Hier wird das Array definiert, das an die HTML-Seite gesendet wird
    my_array = [1, 2, 3, 4, 5]
    return render_template('index.html', my_array=my_array)

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=8080)

