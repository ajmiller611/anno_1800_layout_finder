import customtkinter as ctk
from tkinter import Canvas
from settings import *
from entries_frame import EntriesFrame
from image_frame import LayoutDisplay
from info_frame import InfoPanel, BottomSliderPanel
from PIL import Image, ImageTk


class InitializingFrame(ctk.CTkFrame):
    def __init__(self, parent, initializing_text_var, progress_var):
        super().__init__(master=parent, fg_color=WINDOW_BG_COLOR)
        self.pack(expand=True, fill='both')

        self.original_image = Image.open('images/Anno1800_Wallpaper_City_Lights_1920_1080.jpg')
        self.image = self.original_image
        self.image_ratio = self.image.size[0] / self.image.size[1]
        self.image_tk = ImageTk.PhotoImage(self.image)

        # Widgets
        self.image_canvas = Canvas(self, background=ENTRY_TEXT_COLOR, border=20, highlightthickness=0, relief='sunken')
        self.image_canvas.pack(expand=True, fill='both', padx=50, pady=20)
        self.image_canvas.bind('<Configure>', self.resize_image)

        self.label = ctk.CTkLabel(
            self,
            text='',
            textvariable=initializing_text_var,
            text_color=ENTRY_TEXT_COLOR,
            font=ctk.CTkFont(family=FONT_FAMILY, size=TITLE_FONT_SIZE))
        self.label.pack(fill='both')

        self.progressbar = ctk.CTkProgressBar(
            self,
            variable=progress_var,
            width=300,
            height=30,
            fg_color=SCROLLBAR_HOVER_COLOR,
            progress_color=ENTRY_TEXT_COLOR)
        self.progressbar.pack(fill='y', pady=15)

    def resize_image(self, event):
        self.canvas_width = event.width
        self.canvas_height = event.height

        self.image_canvas.delete('all')
        resized_image = self.image.resize((self.canvas_width, self.canvas_height))
        self.image_tk = ImageTk.PhotoImage(resized_image)
        self.image_canvas.create_image(self.canvas_width / 2, self.canvas_height / 2, image=self.image_tk)


class LayoutFinderFrame(ctk.CTkFrame):
    def __init__(self, parent):
        super().__init__(master=parent, fg_color=WINDOW_BG_COLOR)
        self.pack(expand=True, fill='both')

        # Layout
        self.rowconfigure(0, weight=6, uniform='a')
        self.rowconfigure(1, weight=2, uniform='a')
        self.columnconfigure(0, weight=3, uniform='a')
        self.columnconfigure(2, weight=3, uniform='a')
        self.columnconfigure(1, weight=6, uniform='a')

        # Widgets
        EntriesFrame(self, 0, 0)
        LayoutDisplay(self)
        InfoPanel(self)
        self.top_slide_panel = BottomSliderPanel(self, self.update_button_text)
        self.button = ctk.CTkButton(
            self,
            command=self.top_slide_panel.animate,
            text='\u02C5',
            text_color=PANEL_TEXT_COLOR,
            font=ctk.CTkFont(family=FONT_FAMILY, size=BUTTON_TEXT_SIZE),
            corner_radius=0,
            fg_color=BUTTON_FG_COLOR,
            hover_color=BUTTON_HOVER_COLOR,
            border_width=3,
            border_color=PANEL_TEXT_COLOR,
            bg_color=PANEL_TEXT_COLOR,
            width=50,
            height=20)
        self.button.place(relx=0.475, rely=0.975, relwidth=0.05, relheight=0.05)

    def update_button_text(self, *args):
        if self.button.cget('text') == '\u02C5':
            self.button.configure(text='\u02C4')  # Unicode for the modifier letter up arrowhead
        else:
            self.button.configure(text='\u02C5')  # Unicode for the modifier letter down arrowhead
