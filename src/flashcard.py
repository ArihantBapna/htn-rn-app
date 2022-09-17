from typing import Union


class Flashcard:
    front: str
    back: str
    gist: str
    first: Union[None, str]
    second: Union[None, str]
    headline: str
    _headline_embedding: list
    _embedding: list

    def init(self, front, back, gist, first, second, headline_str, headline_embedding, embedding):
        self.front = front
        self.back = back
        self.gist = gist
        self.headline = headline_str
        self._headline_embedding = headline_embedding
        self._embedding = embedding
        self.first = first
        self.second = second
    
    def get_headline_embedding(self):
        return self._headline_embedding
    
    def get_embedding(self):
        return self._embedding


class Node:
    front: str
    point_out: set
    point_in: set

    def init(self, front, point_out, point_in):
        self.front = front
        self.point_in = point_in
        self.point_out = point_out


    

