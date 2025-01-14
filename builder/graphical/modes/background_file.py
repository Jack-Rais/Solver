import tkinter as tk
from tkinter import filedialog, messagebox
from PIL import Image, ImageTk

from .base_mode import Mode


class BackgroundFile(Mode):

    def __init__(self, **kwargs):

        for key, value in kwargs.items():
            setattr(self, key, value)

        self.ask_for_file()

    
    def set_background_image(self, canvas:tk.Canvas, image_path:str):

        canvas.config(
            bg = None
        )

        image = Image.open(fp = image_path)

        if image.width > image.height:
            new_width = canvas.winfo_width()
            new_height = int((new_width * image.height) / image.width)

            image.thumbnail([new_width, new_height], Image.Resampling.LANCZOS)

        else:
            new_height = canvas.winfo_width()
            new_width = int((new_height * image.height) / image.width)

            image.thumbnail([new_width, new_height], Image.Resampling.LANCZOS)


        self.background = ImageTk.PhotoImage(image)
        im = canvas.create_image(
            (canvas.winfo_width() // 2, canvas.winfo_height() // 2), 
            image = self.background
        )
        self.canvas.lower(im)

        canvas.background_type = 'image'

    
    def set_background(self):

        file_path = filedialog.askopenfilename(
            title="Select a Background",
            filetypes=[("Image files", "*.jpg;*.jpeg;*.png;*.gif;*.bmp;*.tiff")]
        )
        if file_path:
            self.set_background_image(self.canvas, file_path)

    
    def ask_for_file(self):

        if getattr(self.canvas, "background_type", None) == "image":

            response = messagebox.askyesnocancel(
                "Choose Action", "Do you want to select a new background? (Yes to select, No to reset)"
            )

            if response is True:
                self.set_background()

            elif response is False:
                self.background = None
                
                for element in self.canvas.find_all():
                    if self.canvas.type(element) == 'image':
                        self.canvas.delete(element)

                self.canvas.background_type = 'color'

        else:
            self.set_background()

    
    def unbind(self):
        pass


    def pass_args(self):
        
        return {
            'canvas': self.canvas,
            'nodes': self.nodes,
            'background': self.background
        }