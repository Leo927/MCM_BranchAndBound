import unittest
from graph import MCMGraph

class TestMCMGraph(unittest.TestCase):
    def test_add_include(self):
        G = MCMGraph()
        G.add_edges_from([(1,2), (2,3), (2,4), (4,5)])
        G.initialize()
        G.add_include_edge(1,2)
        G.propagate_constraints((1,2))
        self.assertEqual(G.score, 2)


if __name__ == "__main__":
    unittest.main()