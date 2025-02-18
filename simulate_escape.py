from system.visualizer import Visualizer
from utils import get_file

graph = get_file()


root = Visualizer(
    graph = graph
)
root.run()