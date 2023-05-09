import customtkinter as ctk
from tkinter import Canvas
from settings import *
from PIL import Image, ImageTk


class Panel(ctk.CTkFrame):
    def __init__(self, parent, color, row, col, span, text, data):
        super().__init__(master=parent, fg_color=color, corner_radius=0)
        self.grid(row=row, column=col, columnspan=span, sticky='nsew')

        # Widgets
        self.rowconfigure(0, weight=1)
        self.columnconfigure(0, weight=2 if text == 'Space Efficiency' else 1, uniform='a')
        self.columnconfigure(1, weight=1, uniform='a')
        ctk.CTkLabel(
            self,
            text=f'{text}:',
            text_color=PANEL_TEXT_COLOR,
            font=ctk.CTkFont(family=FONT_FAMILY, size=TITLE_FONT_SIZE)).grid(row=0, column=0, sticky='w', padx=5)
        ctk.CTkLabel(
            self,
            text=data,
            text_color=PANEL_TEXT_COLOR,
            font=ctk.CTkFont(family=FONT_FAMILY, size=TITLE_FONT_SIZE)).grid(row=0, column=1, sticky='w', padx=5)


class InfoPanel(ctk.CTkFrame):
    def __init__(self, parent):
        super().__init__(master=parent, fg_color='transparent')
        self.grid(row=0, rowspan=2, column=2, sticky='nsew')

        # Layout
        self.rowconfigure((1, 3, 5, 7), weight=1, uniform='b')
        self.rowconfigure((0, 2, 4, 6), weight=2, uniform='b')
        self.rowconfigure(8, weight=5, uniform='b')
        self.columnconfigure(0, weight=1, uniform='b')
        self.columnconfigure(1, weight=1, uniform='b')

        # Widgets
        ConstructionCostPanel(self, PANEL_BG_COLOR, 0, 0, 2)
        Panel(self, PANEL_BG_COLOR, 2, 0, 1, 'Size', '27x27')
        Panel(self, PANEL_BG_COLOR, 2, 1, 1, 'Tiles', '729')
        Panel(self, PANEL_BG_COLOR, 4, 0, 2, 'Space Efficiency', '79%')
        Panel(self, PANEL_BG_COLOR, 6, 0, 2, 'Production', '8')
        LogoPanel(self)


class ConstructionCostPanel(ctk.CTkFrame):
    def __init__(self, parent, color, row, col, span):
        super().__init__(master=parent, fg_color=color, corner_radius=0)
        self.grid(row=row, column=col, columnspan=span, sticky='nsew')

        # Layout
        self.rowconfigure((0, 1, 2), weight=1, uniform='a')
        self.columnconfigure(0, weight=7, uniform='a')
        self.columnconfigure((1, 4, 7), weight=2, uniform='a')
        self.columnconfigure((2, 5, 8), weight=6, uniform='a')
        self.columnconfigure((3, 6), weight=1, uniform='a')

        # Widgets
        ctk.CTkLabel(
            self,
            text=f'Costs:',
            text_color=PANEL_TEXT_COLOR,
            font=ctk.CTkFont(family=FONT_FAMILY, size=TITLE_FONT_SIZE)).grid(row=0, rowspan=3, column=0,
                                                                             sticky='w', padx=5)

        image = Image.open('icons/Credits.webp')
        image_tkk = ctk.CTkImage(light_image=image, dark_image=image)
        ctk.CTkLabel(
            self,
            text='',
            image=image_tkk).grid(row=0, column=1, sticky='nsew')
        ctk.CTkLabel(
            self,
            text='1.588(23.544)',
            text_color=PANEL_TEXT_COLOR,
            font=ctk.CTkFont(family=FONT_FAMILY, size=INFO_FONT_SIZE)).grid(row=0, column=2, columnspan=7, sticky='w')

        image = Image.open('icons/Timber.webp')
        image_tkk = ctk.CTkImage(light_image=image, dark_image=image)
        ctk.CTkLabel(
            self,
            text='',
            image=image_tkk).grid(row=1, column=1, sticky='nsew')
        ctk.CTkLabel(
            self,
            text='26(20)',
            text_color=PANEL_TEXT_COLOR,
            font=ctk.CTkFont(family=FONT_FAMILY, size=INFO_FONT_SIZE)).grid(row=1, column=2, columnspan=2, sticky='nsew')

        self.middle_dot_separator(self, 1, 3)

        image = Image.open('icons/Bricks.webp')
        image_tkk = ctk.CTkImage(light_image=image, dark_image=image)
        ctk.CTkLabel(
            self,
            text='',
            image=image_tkk).grid(row=1, column=4, sticky='nsew')
        ctk.CTkLabel(
            self,
            text='(20)',
            text_color=PANEL_TEXT_COLOR,
            font=ctk.CTkFont(family=FONT_FAMILY, size=INFO_FONT_SIZE)).grid(row=1, column=5, sticky='nsew',
                                                                            padx=5)

        self.middle_dot_separator(self, 1, 6)

        image = Image.open('icons/Steel_beams.webp')
        image_tkk = ctk.CTkImage(light_image=image, dark_image=image)
        ctk.CTkLabel(
            self,
            text='',
            image=image_tkk).grid(row=1, column=7, sticky='nsew')
        ctk.CTkLabel(
            self,
            text='(80)',
            text_color=PANEL_TEXT_COLOR,
            font=ctk.CTkFont(family=FONT_FAMILY, size=INFO_FONT_SIZE)).grid(row=1, column=8, sticky='nsew')

        image = Image.open('icons/Windows.webp')
        image_tkk = ctk.CTkImage(light_image=image, dark_image=image)
        ctk.CTkLabel(
            self,
            text='',
            image=image_tkk).grid(row=2, column=1, sticky='nsew')
        ctk.CTkLabel(
            self,
            text='(---------)',
            text_color=PANEL_TEXT_COLOR,
            font=ctk.CTkFont(family=FONT_FAMILY, size=INFO_FONT_SIZE)).grid(row=2, column=2, sticky='nsew')

        self.middle_dot_separator(self, 2, 3)

        image = Image.open('icons/Reinforced_concrete.webp')
        image_tkk = ctk.CTkImage(light_image=image, dark_image=image)
        ctk.CTkLabel(
            self,
            text='',
            image=image_tkk).grid(row=2, column=4, sticky='nsew')
        ctk.CTkLabel(
            self,
            text='12',
            text_color=PANEL_TEXT_COLOR,
            font=ctk.CTkFont(family=FONT_FAMILY, size=INFO_FONT_SIZE)).grid(row=2, column=5, sticky='nsew',
                                                                            padx=5)

    def middle_dot_separator(self, parent, row, col):
        ctk.CTkLabel(
            master=parent,
            text='\u00B7',  # Unicode for middle dot character.
            text_color=PANEL_TEXT_COLOR,
            font=ctk.CTkFont(family=FONT_FAMILY, size=TITLE_FONT_SIZE)).grid(row=row, column=col, sticky='nsew')


class LogoPanel(Canvas):
    def __init__(self, parent):
        super().__init__(master=parent, background=WINDOW_BG_COLOR, bd=0, highlightthickness=0, relief='ridge')
        self.grid(row=8, column=0, columnspan=2, sticky='nsew')

        self.original = Image.open('images/anno-1800-key-art-2018.jpg')
        self.image = self.original
        self.image_ratio = self.image.size[0] / self.image.size[1]
        self.image_tk = ImageTk.PhotoImage(self.image)

        self.bind('<Configure>', self.resize_image)

    def resize_image(self, event):
        canvas_ratio = event.width / event.height

        self.canvas_width = event.width
        self.canvas_height = event.height

        if canvas_ratio > self.image_ratio:
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


class BottomSliderPanel(ctk.CTkFrame):
    def __init__(self, parent, update_button):
        super().__init__(master=parent, fg_color=SLIDER_PANEL_BG_COLOR)

        self.start_pos = 0.73
        self.end_pos = 1.03
        self.height = abs(self.start_pos - self.end_pos)

        self.pos = self.start_pos
        self.in_start_pos = ctk.BooleanVar(value=True)
        self.in_start_pos.trace('w', update_button)

        self.place(relx=0.26, rely=self.start_pos, relwidth=0.48, relheight=self.height)

        # Layout
        self.rowconfigure((0, 1), weight=5, uniform='a')
        self.rowconfigure(2, weight=1, uniform='a')
        self.rowconfigure((3, 4), weight=4, uniform='a')
        self.columnconfigure((0, 3, 6), weight=1, uniform='a')
        self.columnconfigure((1, 2, 4, 5), weight=4, uniform='a')

        # Data
        self.width_entry_var = ctk.StringVar()
        self.height_entry_var = ctk.StringVar()

        # Widgets
        ctk.CTkLabel(
            master=self,
            text='Enter The Max Dimension Parameters',
            text_color=PANEL_TEXT_COLOR,
            font=ctk.CTkFont(family=FONT_FAMILY, size=36)).grid(row=0, column=0, columnspan=7, sticky='ns')

        ctk.CTkLabel(
            master=self,
            text='Width:',
            text_color=PANEL_TEXT_COLOR,
            font=ctk.CTkFont(family=FONT_FAMILY, size=TITLE_FONT_SIZE)).grid(row=1, column=1, sticky='nsew')
        ctk.CTkEntry(
            master=self,
            textvariable=self.width_entry_var,
            text_color=PANEL_TEXT_COLOR,
            font=ctk.CTkFont(family=FONT_FAMILY, size=INFO_FONT_SIZE),
            fg_color=PANEL_BG_COLOR,
            border_color=PANEL_TEXT_COLOR).grid(row=1, column=2, sticky='ew')

        ctk.CTkLabel(
            master=self,
            text='Height:',
            text_color=PANEL_TEXT_COLOR,
            font=ctk.CTkFont(family=FONT_FAMILY, size=TITLE_FONT_SIZE)).grid(row=1, column=4, sticky='nsew')
        ctk.CTkEntry(
            master=self,
            textvariable=self.height_entry_var,
            text_color=PANEL_TEXT_COLOR,
            font=ctk.CTkFont(family=FONT_FAMILY, size=INFO_FONT_SIZE),
            fg_color=PANEL_BG_COLOR,
            border_color=PANEL_TEXT_COLOR).grid(row=1, column=5, sticky='ew')

        self.error_label = ctk.CTkLabel(
            master=self,
            text='',
            text_color='red',
            font=ctk.CTkFont(family=FONT_FAMILY, size=INFO_FONT_SIZE))
        self.error_label.grid(row=2, column=2, columnspan=3, sticky='nsew')

        ctk.CTkButton(
            master=self,
            command=self.layout_search,
            text='Search',
            text_color=PANEL_TEXT_COLOR,
            font=ctk.CTkFont(family=FONT_FAMILY, size=INFO_FONT_SIZE),
            fg_color=BUTTON_FG_COLOR,
            hover_color=BUTTON_HOVER_COLOR).grid(row=3, column=2, columnspan=3, sticky='ew')

    def animate(self):
        if self.in_start_pos.get():
            self.animate_down()
        else:
            self.animate_up()

    def animate_up(self):
        if self.pos > self.start_pos:
            self.pos -= 0.008
            self.place(relx=0.26, rely=self.pos, relwidth=0.48, relheight=self.height)
            self.after(10, self.animate_up)
        else:
            self.in_start_pos.set(True)

    def animate_down(self):
        if self.pos < self.end_pos:
            self.pos += 0.008
            self.place(relx=0.26, rely=self.pos, relwidth=0.48, relheight=self.height)
            self.after(10, self.animate_down)
        else:
            self.in_start_pos.set(False)

    def layout_search(self):
        if self.width_entry_var.get().isnumeric() and self.height_entry_var.get().isnumeric():
            self.error_label.configure(text='')
            print(f'searching for {self.width_entry_var.get()}x{self.height_entry_var.get()}')
        else:
            self.error_label.configure(text='Invalid Entry: Only numbers are valid')
        pass




