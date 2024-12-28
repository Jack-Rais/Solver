import tkinter as tk


class Mode:

    def __init__(self, canvas: tk.Canvas,
                       nodes: list[dict] | None = None):
        
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