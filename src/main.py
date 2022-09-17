import os

from flask import Flask
from flask import request
from load_audio import get_response
from get_transcript import get_transcript, get_transcript_from_url
from load_audio import get_response_from_url
import json

app = Flask(__name__)

filename = "Asking Harvard Students If They Ever Sleep.mp3"


@app.route("/")
def hello_world():
    return "Hello"


@app.route("/get_transcript_url")
def load_audio_from_url():
    url = json.loads(request.data).get('url')
    return get_response_from_url(url)

@app.route("/get_transcript")
def load_audio():
    return get_response(filename)

@app.route("/get_prof_transcript")
def get_prof_transcript():
    url = json.loads(request.data).get('url')
    return get_transcript_from_url(url)

@app.route("/prof_transcript")
def prof_transcript():
    return get_transcript(filename)


@app.route("/test")
def test():
    return


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=int(os.environ.get("PORT", 8080)))
