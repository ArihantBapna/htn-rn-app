# compute_graph.py
from typing import Dict, Set, List
from flashcard import Flashcard, Node, Graph
import numpy as np
import pandas as pd
from collections import defaultdict
from sklearn.metrics.pairwise import cosine_similarity
# compute the top 5 edges for every node into a table with sim score rel to other nodes
# sort according to sim score
# going down in the table, attempt to add a given edge
# if adding the edge would result in
#      outgoing edges <= 2 and incoming edges <= 2 for either node, go to next in table
# else, add the edge to set of edges and update each node. if node is satisfied,
# put it in DONE and remove from AVAILABLE
# when all nodes are in DONE we are done
# if table exhausted continue running with expanded table (2x edges per node) 
#      (make sure to ignore edges already in set)

def construct_tree(flashcards: List[Flashcard]) -> Graph:
    """Construct a tree of nodes from a list of Flashcards.
    """
    graph = Graph() 
    for flashcard in flashcards:
        graph.add_node(flashcard)
    
    sim_max = 5
    # sort according to sim score
    # going down in the table, attempt to add a given edge
    # if adding the edge would result in
    #      outgoing edges <= 2 and incoming edges <= 2 for either node, go to next in table
    # else, add the edge to set of edges and update each node. if node is satisfied,
    # put it in DONE and remove from AVAILABLE
    # when all nodes are in DONE we are done
    # if table exhausted continue running with expanded table (2x edges per node)
    #      (make sure to ignore edges already in set)
    done = set()
    available = set(graph.nodes)
    while len(available) > 0:
        simscores = compute_sim_scores(graph, sim_max)
        df = pd.DataFrame(sim_scores)
        if df.size > 0:
            df.sort_values(by=2, axis=0)
        sim_scores = df.values.tolist()

        for edge in sim_scores:
            if edge[0] in done or edge[1] in done:
                continue
            # if adding the edge would result in
            #      outgoing edges > 2 or incoming edges > 2 for either node, go to next in table
            if len(edge[0].point_out) == 2 or len(edge[1].point_in) == 2:
                continue
            else:
                graph.add_edge(edge)
                done.add(edge[0])
                done.add(edge[1])
                available.remove(edge[0])
                available.remove(edge[1])
        sim_max *= 2
        
    return str(graph.graph_to_json())

def compute_sim_scores(graph, depth_limit):
    sim_scores = set()
    # computer the top 5 edges for every node into a table with sim score rel to other nodes
    for node in graph.nodes:
        depth = 0
        for other_node in graph.nodes:
            depth += 1
            if depth > depth_limit:
                break
            if node != other_node:
                sim_scores.add(
                    (node, other_node, cosine_similarity(node.flashcard.get_embedding(),
                     other_node.flashcard.get_embedding())))

    return sim_scores
