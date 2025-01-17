import tkinter as tk
from PIL import ImageFile

from ...network import Network


class Mode:

    nodes:Network
    canvas:tk.Canvas
    background:ImageFile

    def __init__(self, **kwargs):
        
        raise NotImplementedError("__init__ deve essere implementato nella sottoclasse.")
    

    def on_mouse_press(self, event: tk.Event):
        """Gestisce il click del mouse per iniziare l'interazione."""

        raise NotImplementedError("on_mouse_press deve essere implementato nella sottoclasse.")


    def on_mouse_motion(self, event: tk.Event):
        """Gestisce il movimento del mouse durante l'interazione."""

        raise NotImplementedError("on_mouse_motion deve essere implementato nella sottoclasse.")


    def on_mouse_release(self, event: tk.Event):
        """Gestisce il rilascio del mouse durante l'interazione."""

        raise NotImplementedError("on_mouse_release deve essere implementato nella sottoclasse.")


    def unbind(self):
        """Disassocia gli eventi del mouse dalla canvas."""

        raise NotImplementedError("unbind deve essere implementato nella sottoclasse.")
    

    def pass_args(self):
        """Restituisce tutti gli argomenti da passare alla modalità successiva"""

        raise NotImplementedError("pass_args deve essere implementato nella sottoclasse.")