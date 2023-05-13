import customtkinter as ctk
import pandas as pd
from tkinter import Canvas
from settings import *
from data_retriever import convert_data_entry_to_dict
from entries_frame import EntriesFrame
from image_frame import LayoutDisplay
from info_frame import InfoPanel, BottomSliderPanel
from PIL import Image, ImageTk


class InitializingFrame(ctk.CTkFrame):
    def __init__(self, parent, initializing_text_var, progress_var):
        super().__init__(master=parent, fg_color=WINDOW_BG_COLOR)
        self.pack(expand=True, fill='both')

        self.original_image = Image.open(INITIALIZING_FRAME_BG_IMAGE_PATH)
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

        data = pd.read_csv('layout_data.csv')

        # Create the widgets with all layouts in the entries list and the first layout as the initial data displayed.
        self.entries_frame = EntriesFrame(self, data, self.update_layout_image_display, self.update_info_panel)
        self.layout_image_display = LayoutDisplay(self, data.iloc[0]['Image'])
        self.info_panel = InfoPanel(
            self,
            convert_data_entry_to_dict(data.iloc[0]['Cost']),
            data.iloc[0]['Size'] if not pd.isna(data.iloc[0]['Size']) else 'N/A',
            data.iloc[0]['Tiles'] if not pd.isna(data.iloc[0]['Tiles']) else 'N/A',
            data.iloc[0]['Space Efficiency'] if not pd.isna(data.iloc[0]['Space Efficiency']) else 'N/A',
            convert_data_entry_to_dict(data.iloc[0]['Production']))

        self.top_slide_panel = BottomSliderPanel(self, self.update_button_text)
        self.button = ctk.CTkButton(
            self,
            command=self.top_slide_panel.animate,
            text='\u02C5',  # Unicode for the modifier letter down arrowhead
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

    def update_layout_image_display(self, image_path):
        self.layout_image_display.original = Image.open(image_path)
        self.layout_image_display.image = self.layout_image_display.original
        self.layout_image_display.image_ratio = \
            self.layout_image_display.image.size[0] / self.layout_image_display.image.size[1]

        self.layout_image_display.image_tk = ImageTk.PhotoImage(self.layout_image_display.image)

        if self.layout_image_display.canvas_ratio > self.layout_image_display.image_ratio:
            self.layout_image_display.image_height = int(self.layout_image_display.canvas_height)
            self.layout_image_display.image_width = int(self.layout_image_display.image_height
                                                        * self.layout_image_display.image_ratio)
        else:
            self.layout_image_display.image_width = int(self.layout_image_display.canvas_width)
            self.layout_image_display.image_height = int(self.layout_image_display.image_width
                                                         / self.layout_image_display.image_ratio)

        self.layout_image_display.place_image()

    def update_info_panel(self, cost, size, tiles, space_eff, production):
        self.info_panel.update_info_data_display(cost, size, tiles, space_eff, production)

    def update_button_text(self, *args):
        if self.button.cget('text') == '\u02C5':
            self.button.configure(text='\u02C4')  # Unicode for the modifier letter up arrowhead
        else:
            self.button.configure(text='\u02C5')  # Unicode for the modifier letter down arrowhead
