from typing import Union
import numpy as np
import json
from json import JSONEncoder


class Flashcard:
    front: str
    back: str
    gist: str
    first: Union[None, str]
    second: Union[None, str]
    headline: str
    _headline_embedding: list
    _embedding: list
    _average_embedding: Union[None, np.array]

    def __init__(self, front, back, gist, first, second, headline_str, headline_embedding, embedding,
                 average_embedding):
        self.front = front
        self.back = back
        self.gist = gist
        self.headline = headline_str
        self._headline_embedding = headline_embedding
        self._embedding = embedding
        self.first = first
        self.second = second
        self._average_embedding = average_embedding

    def get_headline_embedding(self):
        return self._headline_embedding

    def get_embedding(self):
        return self._embedding

    def get_average_embedding(self):
        return self._average_embedding

    def set_average_embedding(self, average_embedding):
        self._average_embedding = average_embedding

    def flashcard_to_json(self):
        return json.dumps(self, default=lambda o: o.__dict__, sort_keys=True, indent=4)

class FlashcardEncoder(JSONEncoder):
    def default(self, o):
        return o.__dict__


class Node:
    flashcard: Flashcard
    point_out: set
    point_in: set

    def __init__(self, flashcard, point_out, point_in):
        self.flashcard = flashcard
        self.point_in = point_in
        self.point_out = point_out


class NodeEncoder(JSONEncoder):
    def default(self, o):
        return o.__dict__
