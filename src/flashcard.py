class Flashcard:
    front: str
    back: str
    gist: str
    left: str = None
    right: str = None
    _headline: str
    _embedding: list

    def init(self, front, back, gist, headline, embedding, left, right):
        self.front = front
        self.back = back
        self.gist = gist
        self._headline = headline
        self._embedding = embedding
        self.left = left
        self.right = right

    