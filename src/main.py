import os
from flask import Flask
from flask import request
from flask_cors import CORS
from load_audio import get_response_from_url
from get_transcript import get_transcript_from_url
from process_text import get_flashcards
from get_visualization import visualize_data
from compute_graph import compute_graph
import json
from dotenv import load_dotenv

load_dotenv()
cohere_api = os.getenv('cohere')
assembly_api = os.getenv('assembly')

app = Flask(__name__)
CORS(app)


@app.route("/")
def hello_world():
    return "Hello"


@app.route("/get_transcript_url", methods=["POST"])
def load_audio_from_url():
    url = json.loads(request.data).get('url')
    return get_response_from_url(url)


@app.route("/get_prof_transcript", methods=["POST"])
def get_prof_transcript_url():
    url = json.loads(request.data).get('url')
    return get_transcript_from_url(url)


@app.route("/process_text")
def process_text():
    x = get_flashcards("https://firebasestorage.googleapis.com/v0/b/htn-rn-app.appspot.com/o/oJDN2chA8uM6BzbAzbrIR4wisD22%2F166.x-m4a?alt=media&token=55c79b8e-73d9-4b1e-8a71-89ad1a37ca1a")
    for flashcard in x:
        print(flashcard.flashcard_to_json())
    return 'success'


@app.route("/get_visualization")
def get_visualization():
    flashcards = get_flashcards("https://firebasestorage.googleapis.com/v0/b/htn-rn-app.appspot.com/o/oJDN2chA8uM6BzbAzbrIR4wisD22%2FY2Mate.is%20-%20TORONTO%20VLOG%20A%20WEEKEND%20IN%20MY%20LIFE-C6yA9Eh8sLY-48k-1660023393366.mp3?alt=media&token=3eb105ec-aa36-45c4-a1b4-e996b1269803")
    for flashcard in flashcards:
        print(f"\n\n{flashcard.flashcard_to_json()}\n\n")
    return visualize_data(flashcards)

@app.route("/get_visualization_url", methods=["POST"])
def get_visualization_url():
    url = json.loads(request.data).get('url')
    flashcards = get_flashcards(url)
    my_data = visualize_data(flashcards)
    return my_data

@app.route("/get_graph")
def get_graph():
    flashcards = get_flashcards("https://firebasestorage.googleapis.com/v0/b/htn-rn-app.appspot.com/o/oJDN2chA8uM6BzbAzbrIR4wisD22%2FY2Mate.is%20-%20TORONTO%20VLOG%20A%20WEEKEND%20IN%20MY%20LIFE-C6yA9Eh8sLY-48k-1660023393366.mp3?alt=media&token=3eb105ec-aa36-45c4-a1b4-e996b1269803")
    return compute_graph(flashcards)


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=int(os.environ.get("PORT", 8080)))
