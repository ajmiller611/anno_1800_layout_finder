import customtkinter as ctk
from settings import *


class EntriesFrame(ctk.CTkFrame):
    def __init__(self, parent, row, col):
        super().__init__(master=parent, fg_color=WINDOW_BG_COLOR)
        self.grid(row=row, rowspan=2, column=col, sticky='nsew')

        # layout
        self.rowconfigure(0, weight=5, uniform='a')
        self.rowconfigure(1, weight=1, uniform='a')
        self.columnconfigure(0, weight=1, uniform='a')

        # widgets
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

        # widgets
        for index in range(15):
            ctk.CTkFrame(self, fg_color=ENTRY_TEXT_COLOR, height=2).pack(fill='x')
            ListEntry(self)
        ctk.CTkFrame(self, fg_color=ENTRY_TEXT_COLOR, height=2).pack(fill='x')


class ListEntry(ctk.CTkFrame):
    def __init__(self, parent):
        super().__init__(master=parent, fg_color='transparent', corner_radius=0)
        self.pack(fill='both')

        # layout
        self.rowconfigure((0, 1), weight=1, uniform='a')
        self.columnconfigure((0, 2), weight=2, uniform='a')
        self.columnconfigure(1, weight=1, uniform='a')
        self.columnconfigure(3, weight=2, uniform='a')

        # widgets
        self.production_line = ctk.CTkLabel(
            master=self,
            text='Schnapps',
            text_color=ENTRY_TEXT_COLOR,
            font=ctk.CTkFont(family=FONT_FAMILY, size=TITLE_FONT_SIZE, weight='bold'))
        self.production_line.grid(row=0, column=0, columnspan=4, sticky='nsew')

        self.production = ctk.CTkLabel(
            master=self, text='Produces:',
            text_color=ENTRY_TEXT_COLOR,
            font=ctk.CTkFont(family=FONT_FAMILY, size=INFO_FONT_SIZE))
        self.production.grid(row=1, column=0, sticky='nsew', padx=4)

        self.production_data_label = ctk.CTkLabel(
            master=self,
            text='10',
            text_color=ENTRY_TEXT_COLOR,
            font=ctk.CTkFont(family=FONT_FAMILY, size=INFO_FONT_SIZE))
        self.production_data_label.grid(row=1, column=1, sticky='w', padx=5)

        self.space_eff = ctk.CTkLabel(
            master=self,
            text='Space Eff:',
            text_color=ENTRY_TEXT_COLOR,
            font=ctk.CTkFont(family=FONT_FAMILY, size=INFO_FONT_SIZE))
        self.space_eff.grid(row=1, column=2, sticky='nsew')

        self.space_eff_label = ctk.CTkLabel(
            master=self,
            text='90.72%',
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


class SortByPanel(ctk.CTkFrame):
    def __init__(self, parent):
        super().__init__(master=parent, fg_color=PANEL_BG_COLOR, corner_radius=0)
        self.grid(row=1, column=0, sticky='nsew')

        # layout
        self.rowconfigure((0, 1, 2), weight=1, uniform='a')
        self.columnconfigure((0, 2), weight=1, uniform='a')
        self.columnconfigure(1, weight=8, uniform='a')

        # data
        checkbox_state = ctk.StringVar()

        # widgets
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
