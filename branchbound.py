from queue import PriorityQueue
import sys
from graph import MCMGraph
import networkx as nx
import matplotlib.pyplot as plt
from helper import get_logger

class MaxPriorityQueue(PriorityQueue):
    def put(self, item):
        key, value = item
        super(MaxPriorityQueue, self).put((-key, value))
    
    def get(self):
        item = super(MaxPriorityQueue, self).get()
        key, value = item
        return (-key, value)
    

class BranchAndBound:
    def __init__(self, original_state, find_max = True):
        self.global_best = None
        self.global_best_state = None
        self.original_state = original_state

    def find_best(self):
        pq = MaxPriorityQueue()
        pq.put((self.original_state.local_best, self.original_state))
        while(not pq.empty()):
            local_best, current_state = pq.get()
            if current_state.worst_than(self.global_best):
                continue
            next_states = current_state.get_next_states()
            if len(next_states) == 0:
                self.update_best(current_state)
            for next_s in next_states:
                pq.put((next_s.local_best, next_s))
        return self.global_best_state

    def update_best(self,state):
        local_best = state.local_best
        get_logger().debug(f'at leaf, local best = {local_best}, global = {self.global_best}')
            
        if self.global_best == None or local_best > self.global_best:
            self.global_best = local_best
            self.global_best_state = state

if __name__ == "__main__":
    G = MCMGraph()
    random_graph = nx.fast_gnp_random_graph(7, 0.4)
    print(f'graph generate complete')
    G.add_edges_from(random_graph.edges)
    G.initialize()
    bnb = BranchAndBound(G)
    
    best = bnb.find_best()
    best.draw()
    
        
