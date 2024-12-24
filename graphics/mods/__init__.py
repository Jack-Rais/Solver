import tkinter as tk
from typing import Callable

class Mode:

    def __call__(self, canvas:tk.Canvas,
                       nodes:list | None = None):

        raise NotImplementedError("You need to subscribe the method __call__")