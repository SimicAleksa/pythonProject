import tkinter as tk
from tkinter import *
import ctypes
import re
import os
from tkinter import *
import ctypes
import re
import os
from functools import partial

from tkinter import ttk


class CodeEditorFrame(ttk.Frame):
    def __init__(self, parent):
        super().__init__(parent)

        ctypes.windll.shcore.SetProcessDpiAwareness(True)

        self.previousText = ''

        # Define colors for the variouse types of tokens
        region = self.rgb((0, 204, 0))
        item = self.rgb((153, 102, 51))
        positions = self.rgb((0, 204, 255))
        player = self.rgb((255, 51, 204))
        normal = self.rgb((234, 234, 234))
        keywords = self.rgb((234, 95, 95))
        comments = self.rgb((95, 234, 165))
        string = self.rgb((234, 162, 95))
        function = self.rgb((95, 211, 234))
        background = self.rgb((42, 42, 42))
        font = 'Consolas 15'

        # Define a list of Regex Pattern that should be colored in a certain way
        self.repl = [
            ['False|True',keywords],
            ['start_position|final_position', positions],
            ['\(.*?\)', player],
            ['".*?"', string],
            ['<.*?>', region],
            ['\[.*?\]', item],
            ['\'.*?\'', string],
            ['#.*?$', comments],
        ]

        # Make the Text Widget
        # Add a hefty border width so we can achieve a little bit of padding
        self.editArea = Text(
            self,
            background=background,
            foreground=normal,
            insertbackground=normal,
            relief=FLAT,
            borderwidth=30,
            font=font,
            height= 35,
            width= 104
        )

        # Place the Edit Area with the pack method
        self.editArea.pack(
            fill=BOTH,
            expand=1
        )

        # Insert some Standard Text into the Edit Area
        self.editArea.insert('1.0', """<Region> {
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

start_position Region
final_position Region
        """)

        # Bind the KeyRelase to the Changes Function
        self.editArea.bind('<KeyRelease>', self.changes)

        # Bind Control + R to the exec function
        self.bind('<Control-r>', self.execute)

        self.changes()

    # Execute the Programm
    def execute(self,event=None):

        # Write the Content to the Temporary File
        with open('run.py', 'w', encoding='utf-8') as f:
            f.write(self.editArea.get('1.0', END))

        # Start the File in a new CMD Window
        os.system('start cmd /K "python run.py"')

    # Register Changes made to the Editor Content
    def changes(self,event=None):
        # If actually no changes have been made stop / return the function
        if self.editArea.get('1.0', END) == self.previousText:
            return

        # Remove all tags so they can be redrawn
        for tag in self.editArea.tag_names():
            self.editArea.tag_remove(tag, "1.0", "end")

        # Add tags where the search_re function found the pattern
        i = 0
        for pattern, color in self.repl:
            for start, end in self.search_re(pattern, self.editArea.get('1.0', END)):
                self.editArea.tag_add(f'{i}', start, end)
                self.editArea.tag_config(f'{i}', foreground=color)

                i += 1

        self.previousText = self.editArea.get('1.0', END)

    def search_re(self,pattern, text, groupid=0):
        matches = []

        text = text.splitlines()
        for i, line in enumerate(text):
            for match in re.finditer(pattern, line):
                matches.append(
                    (f"{i + 1}.{match.start()}", f"{i + 1}.{match.end()}")
                )

        return matches

    def rgb(self,rgb):
        return "#%02x%02x%02x" % rgb
