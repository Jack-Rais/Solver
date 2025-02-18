from system.updater.updater import Updater
from utils import get_file

graph = get_file()

root = Updater(
    graph = graph
)
root.run()