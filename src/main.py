import os

from flask import Flask
from load_audio import get_response

app = Flask(__name__)


@app.route("/")
def hello_world():
    return "Hello"


@app.route("/hi")
def load_audio():
    return get_response()


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=int(os.environ.get("PORT", 8080)))
