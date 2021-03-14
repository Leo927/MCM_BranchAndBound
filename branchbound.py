from queue import PriorityQueue
import sys
from graph import MCMGraph
import networkx as nx
import time
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
        self.start_time = None
        self.iter_count = 0
        self.complete_time = None

    def find_best(self):
        self.start_time = time.time()
        pq = MaxPriorityQueue()
        pq.put((self.original_state.order, self.original_state))
        while(not pq.empty()):
            order, current_state = pq.get()
            self.iter_count+= 1
            get_logger().debug(f'current_state: {current_state}')
            if current_state.worst_than(self.global_best):
                get_logger().debug(f'current_state is worst than global best: {self.global_best}')
                continue
            next_states = current_state.get_next_states()
            if len(next_states) == 0:
                self.update_best(current_state)
            for next_s in next_states:
                pq.put((next_s.order, next_s))
        self.complete_time = time.time() - self.start_time
        return self.global_best_state

    def update_best(self,state):
        local_best = state.local_best
        get_logger().debug(f'At leaf, local best = {local_best}, global = {self.global_best}')
            
        if self.global_best == None or local_best > self.global_best:
            self.global_best = local_best
            self.global_best_state = state
            get_logger().debug(f'Global best is updated to {self.global_best}')

def experiment(n,p, num_run = 10):
    iterations = []
    runing_times = []
    for i in range(num_run):
        G = MCMGraph()
        random_graph = nx.fast_gnp_random_graph(n, p)
        G.add_edges_from(random_graph.edges)
        G.initialize()
        bnb = BranchAndBound(G)
        best = bnb.find_best()
        iterations.append(bnb.iter_count)
        runing_times.append(bnb.complete_time)

if __name__ == "__main__":
    G = MCMGraph()
    random_graph = nx.fast_gnp_random_graph(100, 0.2)
    print(f'graph generate complete')
    G.add_edges_from(random_graph.edges)
    G.initialize()
    bnb = BranchAndBound(G)
    best = bnb.find_best()
    print(f'(n, m, i, t) = ({G.num_nodes}, {G.num_edges}, {bnb.iter_count}, {bnb.complete_time})')
    best.draw()
    
        
