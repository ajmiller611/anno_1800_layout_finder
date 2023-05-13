import customtkinter as ctk
from tkinter import Canvas
from settings import *
from PIL import Image, ImageTk


def middle_dot_separator(parent, row, col):
    ctk.CTkLabel(
        master=parent,
        text='\u00B7',  # Unicode for middle dot character.
        text_color=PANEL_TEXT_COLOR,
        font=ctk.CTkFont(family=FONT_FAMILY, size=30)).grid(row=row, column=col, sticky='nsw')


class Panel(ctk.CTkFrame):
    def __init__(self, parent, color, row, col, span, text, data):
        super().__init__(master=parent, fg_color=color, corner_radius=0)
        self.grid(row=row, column=col, columnspan=span, sticky='nsew', ipadx=5)

        # Layout
        self.rowconfigure(0, weight=1)

        # To reuse this class for space efficiency, a different weight value is needed due to the length of the text.
        self.columnconfigure(0, weight=2 if text == 'Space Efficiency' else 1, uniform='a')
        self.columnconfigure(1, weight=1, uniform='a')

        # Widgets
        ctk.CTkLabel(
            self,
            text=f'{text}:',
            text_color=PANEL_TEXT_COLOR,
            font=ctk.CTkFont(family=FONT_FAMILY, size=INFO_PANEL_FONT_SIZE)).grid(row=0, column=0, sticky='w', padx=5)

        self.data_label = ctk.CTkLabel(
            self,
            text=data,
            text_color=PANEL_TEXT_COLOR,
            font=ctk.CTkFont(family=FONT_FAMILY, size=INFO_PANEL_FONT_SIZE))
        self.data_label.grid(row=0, column=1, sticky='w', padx=5)


class InfoPanel(ctk.CTkFrame):
    def __init__(self, parent, cost, size, tiles, space_eff, production):
        super().__init__(master=parent, fg_color='transparent')
        self.grid(row=0, rowspan=2, column=2, sticky='nsew')

        # Layout
        self.rowconfigure((1, 3, 5, 7), weight=1, uniform='b')
        self.rowconfigure((0, 2, 4, 6), weight=2, uniform='b')
        self.rowconfigure(8, weight=5, uniform='b')
        self.columnconfigure(0, weight=1, uniform='b')
        self.columnconfigure(1, weight=1, uniform='b')

        # Widgets
        self.construction_cost_panel = ConstructionCostPanel(self, cost)
        self.size_panel = Panel(self, PANEL_BG_COLOR, 2, 0, 1, 'Size', size)
        self.tiles_panel = Panel(self, PANEL_BG_COLOR, 2, 1, 1, 'Tiles', tiles)
        self.space_eff_panel = Panel(self, PANEL_BG_COLOR, 4, 0, 2, 'Space Efficiency', space_eff)
        self.production_panel = ProductionPanel(self, production)
        LogoPanel(self)

    def update_info_data_display(self, cost, size, tiles, space_eff, production):
        # Since the number of data elements varies for construction costs and production, recreate those data frames
        # with the new data. Size, titles, and space efficiency only need their data label's text updated.
        self.construction_cost_panel.create_data_display_frame(cost)
        self.size_panel.data_label.configure(text=size)
        self.tiles_panel.data_label.configure(text=tiles)
        self.space_eff_panel.data_label.configure(text=space_eff)
        self.production_panel.create_data_display_frame(production)


class ConstructionCostPanel(ctk.CTkFrame):
    def __init__(self, parent, cost):
        super().__init__(master=parent, fg_color=PANEL_BG_COLOR, corner_radius=0)
        self.grid(row=0, column=0, columnspan=2, sticky='nsew')

        # Layout
        self.rowconfigure(0, weight=1, uniform='a')
        self.columnconfigure(0, weight=1, uniform='a')
        self.columnconfigure(1, weight=3, uniform='a')

        # Widgets
        ctk.CTkLabel(
            self,
            text=f'Costs:',
            text_color=PANEL_TEXT_COLOR,
            font=ctk.CTkFont(family=FONT_FAMILY, size=INFO_PANEL_FONT_SIZE)).grid(row=0, column=0, sticky='w', padx=5)

        self.data_display_frame = self.create_data_display_frame(cost)

    def create_data_display_frame(self, cost):
        frame = ctk.CTkFrame(self, fg_color=PANEL_BG_COLOR, corner_radius=0)
        frame.grid(row=0, column=1, sticky='nsew')

        # Layout
        frame.rowconfigure((0, 1, 2), weight=1, uniform='a')
        frame.columnconfigure((0, 3), weight=1, uniform='a')
        frame.columnconfigure((1, 4), weight=7, uniform='a')
        frame.columnconfigure(2, weight=3, uniform='a')

        if cost != 'N/A':
            # The credits cost is on its own row since the data could have a lot of digits and needs extra display room.
            # This makes its layout different from the rest of the cost data and gets separated from the looping of the
            # cost data.
            image = Image.open(CONSTRUCTION_MATERIALS_IMAGE_PATH_DICT['Credits'])
            image_tkk = ctk.CTkImage(light_image=image, dark_image=image)
            ctk.CTkLabel(
                frame,
                text='',
                image=image_tkk).grid(row=0, column=0, sticky='e')

            ctk.CTkLabel(
                frame,
                text=cost['Credits'],
                text_color=PANEL_TEXT_COLOR,
                font=ctk.CTkFont(
                    family=FONT_FAMILY, size=INFO_PANEL_FONT_SIZE)).grid(row=0, column=1, columnspan=5, sticky='w',
                                                                         padx=12)

            # For some layouts, the cost data spans three rows. Using a combination of keeping track of the column with
            # a variable and the index of each key, the proper column and row can be determined for the placement of
            # each widget. Since the credits key is in the key list, offset the starting column index.
            column_index = -1
            row_index = 1
            for index, key in enumerate(cost.keys()):
                if key != 'Credits':
                    image = Image.open(CONSTRUCTION_MATERIALS_IMAGE_PATH_DICT[key])
                    image_tkk = ctk.CTkImage(light_image=image, dark_image=image)
                    ctk.CTkLabel(
                        frame,
                        text='',
                        image=image_tkk).grid(row=row_index, column=column_index + index, sticky='e')

                    column_index += 1

                    ctk.CTkLabel(
                        frame,
                        text=cost[key],
                        text_color=PANEL_TEXT_COLOR,
                        font=ctk.CTkFont(
                            family=FONT_FAMILY, size=INFO_PANEL_FONT_SIZE)).grid(row=row_index,
                                                                                 column=column_index + index,
                                                                                 sticky='ew')

                    column_index += 1

                    # Only place a middle dot separator if not at the end of the row or the end of the cost data.
                    # Each cost is represented by key-value pairs. Multiply the length of the keys list by two to get
                    # the total number of cost data points. The credit cost is excluded from this loop but still exists
                    # in the returned keys so subtract two from the total number of data points. Additionally, adjust by
                    # subtracting one for the compensation of index counting. To find when the end of a row occurs,
                    # there are two costs per row or 4 data points. Modulus division can be used to determine the
                    # end of a row.
                    if index * 2 <= (len(cost.keys()) * 2) - 3 and index * 2 % 4 != 0:
                        middle_dot_separator(frame, row_index, column_index + index)

                    # The last column index is four but since an increment occurs for the middle dot separator, five is
                    # when an increment to the row is needed. Reset the column index and offset by the current index.
                    # The column index needs to compensate for the keys index not able to adjust for the new row
                    # occurrence.
                    if column_index + index == 5:
                        column_index = -1 - index
                        row_index += 1

        # Display for when there is empty data.
        else:
            ctk.CTkLabel(
                frame,
                text=cost,
                text_color=PANEL_TEXT_COLOR,
                font=ctk.CTkFont(family=FONT_FAMILY, size=INFO_PANEL_FONT_SIZE)).grid(row=0, rowspan=3, column=1,
                                                                                      sticky='w')

        return frame


class ProductionPanel(ctk.CTkFrame):
    def __init__(self, parent, production):
        super().__init__(master=parent, fg_color=PANEL_BG_COLOR, corner_radius=0)
        self.grid(row=6, column=0, columnspan=2, sticky='nsew')

        # Widgets
        self.rowconfigure(0, weight=1)
        self.columnconfigure((0, 1), weight=1, uniform='a')

        ctk.CTkLabel(
            self,
            text='Production:',
            text_color=PANEL_TEXT_COLOR,
            font=ctk.CTkFont(family=FONT_FAMILY, size=INFO_PANEL_FONT_SIZE)).grid(row=0, column=0, sticky='w', padx=5)

        self.data_display_frame = self.create_data_display_frame(production)

    def create_data_display_frame(self, production):
        frame = ctk.CTkFrame(self, fg_color=PANEL_BG_COLOR, corner_radius=0)
        frame.grid(row=0, column=1, sticky='nsew')

        frame.rowconfigure(0, weight=1)
        frame.columnconfigure((0, 2, 3), weight=1, uniform='a')
        frame.columnconfigure((1, 4), weight=3, uniform='a')

        if production != 'N/A':
            # Since the number of produced goods varies per layout, create widgets based off each key in the production
            # data dictionary.
            column_index = 0
            for index, key in enumerate(production.keys()):
                image = Image.open(PRODUCE_GOODS_IMAGE_PATH_DICT[key])
                image_tkk = ctk.CTkImage(light_image=image, dark_image=image)
                ctk.CTkLabel(
                    frame,
                    text='',
                    image=image_tkk).grid(row=0, column=column_index + index, sticky='e')

                column_index += 1

                ctk.CTkLabel(
                    frame,
                    text=production[key],
                    text_color=PANEL_TEXT_COLOR,
                    font=ctk.CTkFont(
                        family=FONT_FAMILY, size=INFO_PANEL_FONT_SIZE)).grid(row=0, column=column_index + index,
                                                                             sticky='w', padx=5)

                column_index += 1
                if index * 2 <= (len(production.keys()) * 2) - 3:
                    middle_dot_separator(frame, 0, column_index)

        # Display for when there is empty data.
        else:
            ctk.CTkLabel(
                frame,
                text=production,
                text_color=PANEL_TEXT_COLOR,
                font=ctk.CTkFont(family=FONT_FAMILY, size=INFO_PANEL_FONT_SIZE)).grid(row=0, column=1, sticky='nsew')

        return frame


class LogoPanel(Canvas):
    def __init__(self, parent):
        super().__init__(master=parent, background=WINDOW_BG_COLOR, bd=0, highlightthickness=0, relief='ridge')
        self.grid(row=8, column=0, columnspan=2, sticky='nsew')

        self.original = Image.open(LOGO_PANEL_IMAGE_PATH)
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
