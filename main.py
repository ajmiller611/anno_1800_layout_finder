import customtkinter as ctk
from settings import *
from data_retriever import Data
from main_frames import InitializingFrame, LayoutFinderFrame
from threading import Thread

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

        # Setup and extract data by web scrapping.
        self.initializing_text_var = ctk.StringVar(value='Setting up the driver...')
        self.progress_var = ctk.DoubleVar(value=0)
        self.data = Data()

        # Create a new thread for data extracting process.
        self.data_thread = Thread(target=self.data.driver_setup, args=(self.progress_var,))
        self.data_thread.start()
        self.monitor(self.data_thread, 'driver')

        # Widgets
        self.initializing_frame = InitializingFrame(self, self.initializing_text_var, self.progress_var)

    def monitor(self, thread, classification):
        # Monitor the data thread for when the task has been completed.
        if thread.is_alive():
            self.after(50, lambda: self.monitor(thread, classification))

        elif classification == 'driver':
            self.progress_var.set(0)
            self.initializing_text_var.set('Extracting data elements...')
            self.data_thread = Thread(target=self.data.extract_data_elements, args=(self.progress_var,))
            self.data_thread.start()
            self.monitor(self.data_thread, 'elements')

        elif classification == 'elements':
            self.progress_var.set(0)
            self.initializing_text_var.set('Extracting layout images...')
            self.data_thread = Thread(target=self.data.extract_images, args=(self.progress_var,))
            self.data_thread.start()
            self.monitor(self.data_thread, 'images')

        elif classification == 'images':
            self.data.create_data_frame()
            self.initializing_frame.pack_forget()
            LayoutFinderFrame(self)

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
    app = App()
    app.mainloop()
