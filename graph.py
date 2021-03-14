import networkx as nx
import copy
import matplotlib.pyplot as plt
import random
from queue import Queue
from helper import get_logger

score = "score"
included_tag = "included"
excluded_tag = "excluded"


class MCMGraph(nx.Graph):
    def __init__(self):
        super(MCMGraph, self).__init__()
        self.excluded_edges = nx.Graph()
        self.included_edges = nx.Graph()
        self.not_excluded_edges = nx.Graph()
        self.free_edges = nx.Graph()
        self._score = 0

    @property
    def num_edges(self):
        return len(self.edges)

    @property
    def num_nodes(self):
        return len(self.nodes)

    @property
    def order(self):
        return len(self.included_edges)

    def __hash__(self):
        return hash(self.included_edges)

    def __lt__(self, other):
        return self.score < other.score

    def __eq__(self, other):
        same_includes = self.included_edges == other.included_edges
        return same_includes

    def __str__(self):
        return f'nodes: {self.nodes(True)}\nincluded:{self.included_edges.edges}\nexcluded:{self.excluded_edges.edges}\nscore: {self.score}'

    def __repr__(self):
        return str(self)

    def initialize(self):
        self.not_excluded_edges = copy.deepcopy(self)
        self.free_edges = copy.deepcopy(self)
        self.init_score()

    @property
    def local_best(self):
        return self.score

    @property
    def score(self):
        return self._score/2

    def is_matched(self, node):
        return self.included_edges.has_node(node)

    def add_include_edge(self, u, v):
        self.included_edges.add_edge(u, v)
        self.free_edges.remove_edge(u, v)
        self[u][v]['label'] = included_tag
        self.propagate_constraints((u, v))

    def add_exclude_edge(self, u, v):
        if not self.free_edges.has_edge(u, v):
            return
        self.excluded_edges.add_edge(u, v)
        self.free_edges.remove_edge(u, v)
        self[u][v]['label'] = excluded_tag
        self.not_excluded_edges.remove_edge(u, v)

    def init_score(self):
        self._score = 0
        for node in self.nodes:
            node_score = self.get_node_score(node)
            self._score += node_score
            self.nodes[node][score] = node_score

    def worst_than(self, global_best):
        if global_best == None:
            return False
        return self.score <= global_best

    def get_node_score(self, node):
        return int(self.not_excluded_edges.degree(node) >= 1)

    def update_score(self, node):
        new_score = self.get_node_score(node)
        diff = new_score - self.nodes[node][score]
        self._score += diff
        self.nodes[node][score] = new_score

    def propagate_constraints(self, edge):
        for node in edge:
            for other_end in self.neighbors(node):
                if other_end in edge:
                    continue
                self.add_exclude_edge(node, other_end)
                self.update_score(other_end)

    def is_set_edge(self, edge):
        is_included = self.included_edges.has_edge(*edge)
        is_excluded = self.excluded_edges.has_edge(*edge)
        return is_excluded or is_excluded

    def get_next_states(self):
        states = set()
        free_edges = list(self.free_edges.edges())
        if len(free_edges) == 0:
            return states
        edge = free_edges[0]
        next_state = copy.deepcopy(self)
        next_state.add_include_edge(*edge)
        next_state.propagate_constraints(edge)
        states.add(next_state)

        next_state = copy.deepcopy(self)
        next_state.add_exclude_edge(*edge)
        next_state.update_score(edge[0])
        next_state.update_score(edge[1])
        #get_logger().debug(f'Added next state {next_state}')
        states.add(next_state)
        return states

    def draw(self):
        pos = nx.spring_layout(self)
        edges = self.edges()
        colors = [self.label2color(self[u][v]['label']) for u,v in edges]
        weights = [self.label2weight(self[u][v]['label']) for u,v in edges]
        styles = [self.label2style(self[u][v]['label']) for u,v in edges]
        nx.draw(self, pos, edge_color = colors, width = weights, style = styles, with_labels=True)
        edge_labels = nx.get_edge_attributes(self, 'label')

        #nx.draw_networkx_edge_labels(self, pos=pos, edge_labels=edge_labels)
        plt.show()
    
    @classmethod
    def label2color(cls, label):
        mapping = {included_tag: "g", excluded_tag: "r"}
        return mapping[label]
    
    @classmethod
    def label2weight(cls, label):
        mapping = {included_tag: 3, excluded_tag: 0.5}
        return mapping[label]

    @classmethod
    def label2style(cls, label):
        mapping = {included_tag: "solid", excluded_tag: "dashed"}
        return mapping[label]