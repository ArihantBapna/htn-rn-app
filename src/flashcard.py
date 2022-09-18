from typing import Union, List, Tuple
import numpy as np
import json
from json import JSONEncoder


class Flashcard:
    front: str
    back: str
    first: Union[None, str]
    second: Union[None, str]
    headline: str
    _headline_embedding: list
    _embedding: list
    _average_embedding: Union[None, np.array]

    def __init__(self, front, back, first, second, headline_str, headline_embedding, embedding,
                 average_embedding):
        self.front = front
        self.back = back
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
        # Convert every flashcard to a json object, but don't include the embeddings
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
        # Print the node's flashcard json and the lists of points in and out
        print(self.flashcard.flashcard_to_json())
        print(f"Points in:{self.point_in})")
        print(f"Points out:{self.point_out})")


class NodeEncoder(JSONEncoder):
    def default(self, o):
        return o.__dict__


class Graph:
    nodes: List[Node]
    edges: List[Tuple[Node]]  # list of tuples of nodes actually

    def __init__(self, nodes = [], edges = []):
        self.nodes = nodes
        self.edges = edges

    def graph_to_json(self):
        # Convert every node to a json object, but don't include the embeddings
        flashcards = [n.flashcard.flashcard_to_json() for n in self.nodes]
        return str(json.dumps(flashcards))
        
    
    def add_node(self, node):
        self.nodes.append(node)
    
    def add_edge(self, edge):
            edge[0].point_out.add(edge[1])
            edge[1].point_in.add(edge[0])
            # update first and/or second of node
            if edge[0].flashcard.first is None:
                edge[0].flashcard.first = edge[1].flashcard.front
            elif edge[0].flashcard.second is None:
                edge[0].flashcard.second = edge[1].flashcard.front
 
            self.edges.append(edge)
