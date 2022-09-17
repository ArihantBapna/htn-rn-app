class Flashcard:
    front: str
    back: str
    gist: str
    left: str = None
    right: str = None
    headline: str
    _headline: list[float]
    _embedding: list[list[float]]

    def init(self, front, back, gist, left, right, headline_str, headline_embed, embedding):
        self.front = front
        self.back = back
        self.gist = gist
        self.headline = headline_str
        self._headline = headline_embed
        self._embedding = embedding
        self.left = left
        self.right = right

    