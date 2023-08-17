import tkinter as tk
from tkinter import *
import ctypes
import re
import os
from functools import partial

from tkinter import ttk

ctypes.windll.shcore.SetProcessDpiAwareness(True)


class CodeEditorFrame(ttk.Frame):
    def __init__(self, parent):
        super().__init__(parent)

        # adding scrollbar
        scrollbar = Scrollbar(self)

        # packing scrollbar
        scrollbar.pack(side=RIGHT,
                       fill=Y)

        self.text_info = Text(self,
                         yscrollcommand=scrollbar.set)
        self.text_info.pack(fill=BOTH)

        # configuring the scrollbar
        scrollbar.config(command=self.text_info.yview)
        data = """<Region> {
    properties...
    connections...
    requirements...
}

[Item] {
    properties...
    isStatic...
}

(Player) {
    properties...
}

start_position [Region]
final_position [Region]
                    """
        self.text_info.insert("1.0", data)
        # Bind arrow key events
        self.text_info.bind("<Up>", self.move_cursor_up)
        self.text_info.bind("<Down>", self.move_cursor_down)

        self.current_cursor_position = self.text_info.index(tk.CURRENT)

    def move_cursor_up(self, event):
        new_cursor_position = self.text_info.index(f"{self.current_cursor_position} linestart - 1 line")
        if new_cursor_position != "1.0":
            self.current_cursor_position = new_cursor_position
            self.highlight_selected_line(self.current_cursor_position)

    def move_cursor_down(self, event):
        # Check if Enter key is pressed
        if event.keysym == "Return":
            new_cursor_position = self.text_info.index(f"{self.current_cursor_position} lineend + 1 line")
        else:
            new_cursor_position = self.text_info.index(f"{self.current_cursor_position} lineend + 1 line")

        last_line = self.text_info.index("end-1c linestart")
        if new_cursor_position != last_line:
            self.current_cursor_position = new_cursor_position
            self.highlight_selected_line(self.current_cursor_position)

    def highlight_selected_line(self, cursor_position):
        self.text_info.tag_remove("selected_row", "1.0", "end")
        self.text_info.tag_add("selected_row", f"{cursor_position} linestart", f"{cursor_position} lineend + 1 char")
        self.text_info.tag_configure("selected_row", background="lightgray")