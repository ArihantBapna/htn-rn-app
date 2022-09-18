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
        ## Convert every flashcard to a json object, but don't include the embeddings
        stripped = self.__dict__.copy() # copy the dict so we don't modify the original
        del stripped["_headline_embedding"]
        del stripped["_embedding"]
        del stripped["_average_embedding"]
        return json.dumps(stripped, cls=FlashcardEncoder)


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
    
    def print_node(self):
        ## Print the node's flashcard json and the lists of points in and out
        print(self.flashcard.flashcard_to_json())
        print(f"Points in:{self.point_in})")
        print(f"Points out:{self.point_out})")

class NodeEncoder(JSONEncoder):
    def default(self, o):
        return o.__dict__
