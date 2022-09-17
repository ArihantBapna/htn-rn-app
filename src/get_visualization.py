from typing import Dict, Set
from flashcard import Flashcard, Node
from process_text import get_flashcards
import numpy as np
import pandas as pd
from collections import defaultdict

filename = "Asking Harvard Students If They Ever Sleep.mp3"


def visualize_data():
    # average flashcards
    flashcards = get_flashcards()
    flashcard_vectors = {}
    for flashcard in flashcards:
        embeddings_to_avg = [np.array(flashcard.headline)]
        embeddings = flashcard.get_embedding()
        for embedding in embeddings:
            embeddings_to_avg.append(np.array(embedding))
        avg = np.mean(embeddings_to_avg, axis=0)
        flashcard_vectors[flashcard] = avg
        flashcard.set_average_embedding(avg)

    # add .first and .second values to flashcards
    assign_first_second(flashcard_vectors)

    # verify that the graph is connected
    flashcard_dict = {flashcard.front: flashcard for flashcard in flashcards}  # {str : Flashcard}
    nodes = initialize_nodes(flashcards, flashcard_dict)
    lonely, edges = determine_lonely_popular_fan(nodes)
    adjust_graph(lonely, edges)

    # rank nodes by # of input nodes
    return rank_nodes(nodes)


def assign_first_second(flashcard_vectors: Dict[Flashcard, np.array]):
    """Assign .first and .second Flashcards to every Flashcard in flashcard_vectors.

    Equation: Cos(x, y) = x . y / ||x|| * ||y||
    """
    for flashcard, flashcard_vector in flashcard_vectors:
        corresponding_similarities = {}
        for other_front, other_vector in flashcard_vectors:
            if flashcard != other_front:  # don't compare the same node to itself
                cos_val = np.dot(flashcard_vector, other_vector) / (flashcard_vector.size * other_vector.size)
                corresponding_similarities[other_front] = cos_val

        # get top two
        first, second = get_top_two_vectors(corresponding_similarities)
        flashcard.first = first
        flashcard.second = second

    return


def get_top_two_vectors(corresponding_similarities: Dict[Flashcard, np.array]):
    first = ['', 0]
    second = ['', 0]
    for front, cos_val in corresponding_similarities:
        if cos_val >= first[1]:
            first = [front, cos_val]
        elif cos_val >= second[1]:
            second = [front, cos_val]
    return first, second


def initialize_nodes(flashcards: Set[Flashcard], flashcard_dict: Dict[str, Flashcard]):
    """Iterate over flashcards to create nodes: Set[Nodes].
    """
    temp_nodes = {}
    for flashcard in flashcards:
        corresponding_node = Node(flashcard, {flashcard.first, flashcard.second}, set())
        temp_nodes[flashcard] = corresponding_node

    for flashcard, node in temp_nodes:
        first = flashcard_dict[flashcard.first]  # type(first) == Flashcard
        first_node = temp_nodes[first]  # type(first_node) = Node
        temp_nodes[first].point_in.add(first_node)  # Node points to Node

        second = flashcard_dict[flashcard.second]
        second_node = temp_nodes[second]
        temp_nodes[second].point_in.add(second_node)

    nodes = {node for _, node in temp_nodes}
    return nodes


def determine_lonely_popular_fan(nodes: Set[Node]):
    """Return a set of lonely Nodes and a set of edges (fan Node -> popular Node).
    """
    lonely = set()
    edges = set()
    for node in nodes:
        if len(node.point_in) == 0:
            lonely.add(node)

        if len(node.point_in) >= 2:
            for node_in in node.point_in:
                edges.add((node_in, node))  # Node_in (fan) -> Node (popular)

    return lonely, edges


def rank_fan_nodes(lonely_node: Node, edges: Set[tuple]):
    """Return a list of Nodes corresponding to the Flashcards that are most semantically similar to lonely_node's
    Flashcard.
    """
    lst = []
    for fan_node, popular_node in edges:
        fan_avg_embedding = fan_node.flashcard.get_average_embedding()
        lonely_avg_embedding = lonely_node.flashcard.get_average_embedding()
        cos_val = np.dot(fan_avg_embedding, lonely_avg_embedding) / (fan_avg_embedding.size * lonely_avg_embedding.size)
        lst.append([fan_node, popular_node, cos_val])

    df = pd.DataFrame(lst)
    df.sort_values(by=2, axis=0)
    return df.values.tolist()


def adjust_graph(lonely: Set[Node], edges: Set[tuple]):
    """Adjust graph:
        - determine which fan Node's Flashcard (index 0 in each tuple of edges) is the most semantically similar to the
            lonely Node
        - Assert its corresponding popular Node has point_in >= 2; else try (a) again after removing edge from set
        - After finding appropriate edge, remove pointers and add new edge
        - If len(popular Node.point_in) < 2, remove all edges that contain it from set
    """
    for lonely_node in lonely:
        rank = rank_fan_nodes(lonely_node, edges)
        for i in range(len(rank)):
            fan_node, popular_node = rank[i][0], rank[i][1]
            if len(fan_node.point_in) >= 2:
                if fan_node.flashcard.first == popular_node.flashcard.front:
                    fan_node.flashcard.first = lonely_node.flashcard.front
                    lonely_node.point_in.add(fan_node)
                elif fan_node.flashcard.second == popular_node.flashcard.front:
                    fan_node.flashcard.second = lonely_node.flashcard.front
                    lonely_node.point_in.add(fan_node)
                else:
                    print("Oopsie!")
                fan_node.point_out.remove(popular_node)
                popular_node.point_in.remove(fan_node)

            else:
                edges.remove((fan_node, popular_node))


def rank_nodes(nodes: Set[Node]):
    """Return a list of nodes in order of point_in Nodes there are.
    """
    m = 0
    d = defaultdict(list)
    lst = []
    for node in nodes:
        d[len(node.point_in)].append(node.flashcard.front)
        if len(node.point_in) > m:
            m = len(node.point_in)
    for i in range(m):
        if i in d:
            lst.extend(d[i])
    return lst