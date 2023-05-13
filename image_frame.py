import pandas as pd
from tkinter import Canvas
from settings import *
from PIL import Image, ImageTk


class LayoutDisplay(Canvas):
    def __init__(self, parent, image_path):
        super().__init__(master=parent, background=WINDOW_BG_COLOR, bd=0, highlightthickness=0, relief='ridge')
        self.grid(row=0, rowspan=2, column=1, sticky='nsew', padx=8)

        self.original = Image.open(image_path)
        self.image = self.original
        self.image_ratio = self.image.size[0] / self.image.size[1]
        self.image_tk = ImageTk.PhotoImage(self.image)

        self.bind('<Configure>', self.resize_image)

    def resize_image(self, event):
        self.canvas_ratio = event.width / event.height

        self.canvas_width = event.width
        self.canvas_height = event.height

        if self.canvas_ratio > self.image_ratio:
            self.image_height = int(event.height)
            self.image_width = int(self.image_height * self.image_ratio)
        else:
            self.image_width = int(event.width)
            self.image_height = int(self.image_width / self.image_ratio)

        self.place_image()

    def place_image(self):
        self.delete('all')
        resized_image = self.image.resize((self.image_width, self.image_height))
        self.image_tk = ImageTk.PhotoImage(resized_image)
        self.create_image(self.canvas_width / 2, self.canvas_height / 2, image=self.image_tk)

