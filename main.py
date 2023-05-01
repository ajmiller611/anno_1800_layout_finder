import customtkinter as ctk
from settings import *
from entries_frame import EntriesFrame
from image_frame import LayoutDisplay
from info_frame import InfoPanel, BottomSliderPanel
from data_retriever import Data

# Import Windows dynamic link library and C data type converter libraries.
try:
    from ctypes import windll, byref, sizeof, c_int
except:
    pass


class App(ctk.CTk):
    def __init__(self):
        super().__init__(fg_color=WINDOW_BG_COLOR)
        self.geometry(f'{WINDOW_SIZE[0]}x{WINDOW_SIZE[1]}+{self.get_screen_offset()[0]}+{self.get_screen_offset()[1]}')
        self.minsize(WINDOW_SIZE[0], WINDOW_SIZE[1])
        self.iconbitmap('empty.ico')
        self.title('')
        self.change_title_bar_color()

        # initialize
        Data()

        # layout
        self.rowconfigure(0, weight=6, uniform='a')
        self.rowconfigure(1, weight=2, uniform='a')
        self.columnconfigure(0, weight=3, uniform='a')
        self.columnconfigure(2, weight=3, uniform='a')
        self.columnconfigure(1, weight=6, uniform='a')

        # widgets
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

        self.mainloop()

    def update_button_text(self, *args):
        if self.button.cget('text') == '\u02C5':
            self.button.configure(text='\u02C4')  # unicode for the modifier letter up arrowhead
        else:
            self.button.configure(text='\u02C5')  # unicode for the modifier letter down arrowhead

    def get_screen_offset(self):
        # On startup, find offset to center the window on the screen.
        try:
            number_of_monitors = windll.user32.GetSystemMetrics(80)
            virtual_screen = windll.user32.GetSystemMetrics(78), windll.user32.GetSystemMetrics(79)
            x_offset = (virtual_screen[0] // 2) // number_of_monitors - (WINDOW_SIZE[0] // 2)
            y_offset = (virtual_screen[1] // 2) - (WINDOW_SIZE[1] // 2)
            return x_offset, y_offset
        except:
            pass
        # Return zero values if the user is not using Windows OS.
        return 0, 0

    def change_title_bar_color(self):
        # On Windows OS, change the title bar color.
        try:
            HWND = windll.user32.GetParent(self.winfo_id())
            DWMWA_ATTRIBUTE = 35  # title bar color attribute
            windll.dwmapi.DwmSetWindowAttribute(HWND, DWMWA_ATTRIBUTE, byref(c_int(TITLE_BAR_HEX_COLOR)), sizeof(c_int))
        except:
            pass


if __name__ == '__main__':
    App()
