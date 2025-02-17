import networkx as nx
import pickle

from system.solver.modifier import System
from system.solver import Solver


with open('graph_saved.pkl', 'rb') as file:
    graph:nx.Graph = pickle.load(file)

sys = System()
graph = sys.normalize_v1_graph(graph)

p = Solver(graph).solve_every_room(graph)
print(p)