import re
import customtkinter as ctk
from settings import *
import pandas as pd
from PIL import Image


class EntriesFrame(ctk.CTkFrame):
    def __init__(self, parent, row, col):
        super().__init__(master=parent, fg_color=WINDOW_BG_COLOR)
        self.grid(row=row, rowspan=2, column=col, sticky='nsew')

        # Layout
        self.rowconfigure(0, weight=5, uniform='a')
        self.rowconfigure(1, weight=1, uniform='a')
        self.columnconfigure(0, weight=1, uniform='a')

        # Widgets
        ListEntryPanel(self)
        SortByPanel(self)


class ListEntryPanel(ctk.CTkScrollableFrame):
    def __init__(self, parent):
        super().__init__(
            master=parent,
            fg_color='transparent',
            scrollbar_button_color=ENTRY_TEXT_COLOR,
            scrollbar_button_hover_color=SCROLLBAR_HOVER_COLOR)
        self.grid(row=0, column=0, sticky='nsew')

        # Data
        self.title_text_var = ''
        self.production_var = ''
        self.space_eff_var = ''
        self.data = self.get_data()

        # Widgets
        for index in range(self.data.shape[0]):
            ctk.CTkFrame(self, fg_color=ENTRY_TEXT_COLOR, height=2).pack(fill='x')
            ListEntry(
                self,
                self.data['Name'][index],
                self.format_production_text(index),
                self.data['Space Efficiency'][index] if isinstance(self.data['Space Efficiency'][index], str) else 'N/A')
        ctk.CTkFrame(self, fg_color=ENTRY_TEXT_COLOR, height=2).pack(fill='x')

    def get_data(self):
        usecols = ['Name', 'Production', 'Space Efficiency']
        return pd.read_csv('layout_data.csv', usecols=usecols)

    def format_production_text(self, index):
        # Convert the string in the data file to a dictionary.
        production_dict = {}

        # Production data that is empty is represented by {}
        if self.data['Production'][index] != '{}':

            data_string = self.data['Production'][index]
            # remove all whitespace
            data_string = re.sub(r"\s+", "", data_string)
            # remove curly brackets
            data_string = data_string.replace('{', '')
            data_string = data_string.replace('}', '')

            # Since the string in the data file already had the syntax of a dictionary, search for substrings that are
            # surrounded by single quotes. The key-value pairs can then be extracted and put into a dictionary.
            while data_string:
                # Using a regular expression, match any character and all characters between single quotes.
                match = re.search("\'.*?\'", data_string)

                # Remove the single quotes from the matched string.
                key = match.group().replace("'", "")

                # Remove the matched string from the data string by using slicing.
                data_string = data_string[match.span()[1]:]

                # Repeat for the value.
                match = re.search("\'.*?\'", data_string)
                value = match.group().replace("'", "")
                data_string = data_string[match.span()[1]:]

                # Add the key-value pair to the dictionary.
                production_dict[key] = value

        return production_dict


class ListEntry(ctk.CTkFrame):
    def __init__(self, parent, title_text_var, production_var, space_eff_var):
        super().__init__(master=parent, fg_color='transparent', corner_radius=0)
        self.pack(fill='both')

        # Layout
        self.rowconfigure((0, 1), weight=1, uniform='a')
        self.columnconfigure((0, 2), weight=2, uniform='a')
        self.columnconfigure(1, weight=3, uniform='a')
        self.columnconfigure(3, weight=2, uniform='a')

        # Widgets
        self.production_line = ctk.CTkLabel(
            master=self,
            text=title_text_var,
            text_color=ENTRY_TEXT_COLOR,
            font=ctk.CTkFont(family=FONT_FAMILY, size=TITLE_FONT_SIZE, weight='bold'))
        self.production_line.grid(row=0, column=0, columnspan=4, sticky='nsew')

        self.production = ctk.CTkLabel(
            master=self, text='Produces:',
            text_color=ENTRY_TEXT_COLOR,
            font=ctk.CTkFont(family=FONT_FAMILY, size=INFO_FONT_SIZE))
        self.production.grid(row=1, column=0, sticky='nsew')

        ProductionDataFrame(self, production_var, self.selected)

        self.space_eff = ctk.CTkLabel(
            master=self,
            text='Space Eff:',
            text_color=ENTRY_TEXT_COLOR,
            font=ctk.CTkFont(family=FONT_FAMILY, size=INFO_FONT_SIZE))
        self.space_eff.grid(row=1, column=2, sticky='nsew')

        self.space_eff_label = ctk.CTkLabel(
            master=self,
            text=space_eff_var,
            text_color=ENTRY_TEXT_COLOR,
            font=ctk.CTkFont(family=FONT_FAMILY, size=INFO_FONT_SIZE))
        self.space_eff_label.grid(row=1, column=3, sticky='nsew')

        self.bind_all_widgets()

    def bind_all_widgets(self):
        self.bind('<Button>', self.selected)
        for child in self.winfo_children():
            child.bind('<Button>', self.selected)

    def selected(self, event):
        print(event)
        print('selected')
        pass


class ProductionDataFrame(ctk.CTkFrame):
    def __init__(self, parent, production_data, selected_func):
        super().__init__(master=parent, fg_color=WINDOW_BG_COLOR)
        self.grid(row=1, column=1, sticky='nsew', padx=5)

        # Check for empty production data.
        if production_data:
            self.rowconfigure(0, weight=1)

            # Set up the grid layout depending on how many goods the Anno 1800 layout produces.
            if len(production_data.keys()) > 1:
                self.columnconfigure((0, 3), weight=3, uniform='a')
                self.columnconfigure(2, weight=1, uniform='a')
                self.columnconfigure((1, 4), weight=3, uniform='a')
            else:
                self.columnconfigure(0, weight=1, uniform='a')
                self.columnconfigure(1, weight=3, uniform='a')

            # Place the widgets in the correct column based on how many goods the layout produces. Using a variable to
            # keep track of the column index and the index of the enumeration of the keys will return the correct column
            # index.
            column_index = 0
            for index, key in enumerate(production_data.keys()):
                image = Image.open(PRODUCE_GOODS_IMAGE_PATH_DICT[key])
                image_tk = ctk.CTkImage(light_image=image, dark_image=image)
                ctk.CTkLabel(
                    self,
                    text='',
                    image=image_tk).grid(row=0, column=column_index + index, sticky='nse')

                column_index += 1

                ctk.CTkLabel(
                    master=self,
                    text=production_data[key],
                    text_color=ENTRY_TEXT_COLOR,
                    font=ctk.CTkFont(family=FONT_FAMILY, size=INFO_FONT_SIZE)).grid(row=0, column=column_index + index,
                                                                                    sticky='nsw', padx=3)

                # Add middle dot separator unless it's the last value.
                if index != len(production_data.values()) - 1:
                    column_index += 1
                    ctk.CTkLabel(
                        master=self,
                        text='\u00B7',  # Unicode for middle dot character.
                        text_color=ENTRY_TEXT_COLOR,
                        font=ctk.CTkFont(family=FONT_FAMILY, size=INFO_FONT_SIZE)).grid(row=0,
                                                                                        column=column_index + index,
                                                                                        sticky='nsew')
        else:
            ctk.CTkLabel(
                master=self,
                text='N\\A',
                text_color=ENTRY_TEXT_COLOR,
                font=ctk.CTkFont(family=FONT_FAMILY, size=INFO_FONT_SIZE)).pack()

        self.bind_all_widgets(selected_func)

    def bind_all_widgets(self, selected_func):
        self.bind('<Button>', selected_func)
        for child in self.winfo_children():
            child.bind('<Button>', selected_func)


class SortByPanel(ctk.CTkFrame):
    def __init__(self, parent):
        super().__init__(master=parent, fg_color=PANEL_BG_COLOR, corner_radius=0)
        self.grid(row=1, column=0, sticky='nsew')

        # Layout
        self.rowconfigure((0, 1, 2), weight=1, uniform='a')
        self.columnconfigure((0, 2), weight=1, uniform='a')
        self.columnconfigure(1, weight=8, uniform='a')

        # Data
        checkbox_state = ctk.StringVar()

        # Widgets
        self.sort_by_label = ctk.CTkLabel(
            master=self,
            text='Sort Entries By:',
            text_color=PANEL_TEXT_COLOR,
            font=ctk.CTkFont(family=FONT_FAMILY, size=SORT_CHECKBOX_TITLE_FONT_SIZE, weight='bold'))
        self.sort_by_label.grid(row=0, column=0, columnspan=3, sticky='nsew')

        self.production = ctk.CTkCheckBox(
            master=self,
            command=self.production_sorting,
            text='Production per minute',
            text_color=PANEL_TEXT_COLOR,
            font=ctk.CTkFont(family=FONT_FAMILY, size=SORT_CHECKBOX_FONT_SIZE),
            border_color=PANEL_TEXT_COLOR,
            hover_color=SORT_CHECKBOX_HIGHLIGHT_COLOR,
            fg_color=PANEL_TEXT_COLOR,
            checkmark_color=PANEL_BG_COLOR,
            variable=checkbox_state,
            onvalue='production',
            offvalue='space_eff')
        self.production.grid(row=1, column=1, sticky='nsew')

        self.space_eff = ctk.CTkCheckBox(
            master=self,
            command=self.space_eff_sorting,
            text='Space Efficiency',
            text_color=PANEL_TEXT_COLOR,
            font=ctk.CTkFont(family=FONT_FAMILY, size=SORT_CHECKBOX_FONT_SIZE),
            border_color=PANEL_TEXT_COLOR,
            hover_color=SORT_CHECKBOX_HIGHLIGHT_COLOR,
            fg_color=PANEL_TEXT_COLOR,
            checkmark_color=PANEL_BG_COLOR,
            variable=checkbox_state,
            onvalue='space_eff',
            offvalue='production')
        self.space_eff.grid(row=2, column=1, sticky='nsew')

    def production_sorting(self):
        pass

    def space_eff_sorting(self):
        pass
