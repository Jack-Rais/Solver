from system.updater.updater import Updater
import pickle


with open('graph_saved.pkl', 'rb') as file:
    graph = pickle.load(file)



root = Updater(graph = graph)
root.run()