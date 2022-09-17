import os

from flask import Flask
from load_audio import get_response
from get_transcript import get_transcript

app = Flask(__name__)

filename = "Asking Harvard Students If They Ever Sleep.mp3"


@app.route("/")
def hello_world():
    return "Hello"


@app.route("/get_transcript")
def load_audio():
    return get_response(filename)


@app.route("/prof_transcript")
def prof_transcript():
    return get_transcript(filename)


@app.route("/test")
def test():
    return


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=int(os.environ.get("PORT", 8080)))
