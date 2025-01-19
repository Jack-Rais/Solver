import tkinter as tk
import networkx as nx
import pickle


with open('graph_saved.pkl', 'rb') as file:
    graph:nx.Graph = pickle.load(file)


digraph = graph.to_directed()

digraph.