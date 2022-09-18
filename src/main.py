import os

from flask import Flask
from flask import request
from flask_cors import CORS
from load_audio import get_response
from get_transcript import get_transcript, get_transcript_from_url
from load_audio import get_response_from_url
from process_text import get_flashcards
from get_visualization import visualize_data
import json

app = Flask(__name__)
CORS(app)

filename = "Asking Harvard Students If They Ever Sleep.mp3"


@app.route("/")
def hello_world():
    return "Hello"


@app.route("/get_transcript_url", methods=["POST"])
def load_audio_from_url():
    url = json.loads(request.data).get('url')
    return get_response_from_url(url)


@app.route("/get_transcript")
def load_audio():
    return get_response(filename)


@app.route("/get_prof_transcript", methods=["POST"])
def get_prof_transcript_url():
    url = json.loads(request.data).get('url')
    return get_transcript_from_url(url)


@app.route("/prof_transcript")
def get_prof_transcript():
    return get_transcript(filename)


@app.route("/process_text")
def process_text():
    x = get_flashcards("https://firebasestorage.googleapis.com/v0/b/htn-rn-app.appspot.com/o/oJDN2chA8uM6BzbAzbrIR4wisD22%2F166.x-m4a?alt=media&token=55c79b8e-73d9-4b1e-8a71-89ad1a37ca1a")
    for flashcard in x:
        print(flashcard.flashcard_to_json())
    return 'success'


@app.route("/get_visualization")
def get_visualization():
    # flashcards = get_flashcards("https://firebasestorage.googleapis.com/v0/b/htn-rn-app.appspot.com/o/oJDN2chA8uM6BzbAzbrIR4wisD22%2F166.x-m4a?alt=media&token=55c79b8e-73d9-4b1e-8a71-89ad1a37ca1a")
    flashcards = get_flashcards("https://firebasestorage.googleapis.com/v0/b/htn-rn-app.appspot.com/o/oJDN2chA8uM6BzbAzbrIR4wisD22%2FVery%20Nice%2010%20min%20audio.mp3?alt=media&token=6ad43591-762e-46f2-a52b-7b040479aff1")
    for flashcard in flashcards:
        print(f"\n\n{flashcard.flashcard_to_json()}\n\n")
    return visualize_data(flashcards)


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=int(os.environ.get("PORT", 8080)))
