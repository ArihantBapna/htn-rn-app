import os

from flask import Flask
from load_audio import get_response
<<<<<<< HEAD
from get_prof_transcript import generate_prof_transcript
=======
from get_transcript import generate_prof_transcript
>>>>>>> cef976c3555cfffe79133909c9357ab8d09c3d67

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
    return generate_prof_transcript(filename)


@app.route("/test")
def test():
<<<<<<< HEAD
    speaker_to_str = generate_prof_transcript(filename)
    return speaker_to_str 
=======
    return generate_prof_transcript(filename)
    # return get_prof_embedding(speaker_to_str)
>>>>>>> cef976c3555cfffe79133909c9357ab8d09c3d67


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=int(os.environ.get("PORT", 8080)))
