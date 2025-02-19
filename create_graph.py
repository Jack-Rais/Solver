from builder import Builder
from datetime import datetime

root = Builder()
root.run()

root.save("graph_saved" + datetime.now().strftime("%Y-%m-%d_%H-%M-%S") + ".pkl")