from tkinter import *
import ctypes
import re
import tkinter.font as tkfont

from tkinter import ttk,filedialog


class CodeEditorFrame(ttk.Frame):
    def __init__(self, parent,content=None):
        super().__init__(parent)

        ctypes.windll.shcore.SetProcessDpiAwareness(True)

        self.previousText = ''

        # Define colors for the variouse types of tokens
        region = self.rgb((0, 204, 0))
        item = self.rgb((153, 102, 51))
        positions = self.rgb((0, 204, 255))
        player = self.rgb((255, 51, 204))
        normal = self.rgb((234, 234, 234))
        trueFalse = self.rgb((234, 95, 95))
        comments = self.rgb((95, 234, 165))
        string = self.rgb((234, 162, 95))
        commonwords = self.rgb((153, 102, 255))
        background = self.rgb((42, 42, 42))
        font = 'Consolas 15'

        # Define a list of Regex Pattern that should be colored in a certain way
        self.repl = [
            ['(^| )(False|True)', trueFalse],
            ['(^| )(start_position|final_position)', positions],
            ['(^|\t| )(portrayal|contains|N|S|W|E|requirements|isStatic|activation|health|heal|score|inventory|position)',
             commonwords],
            ['\(.*?\)', player],
            ['<.*?>', region],
            ['\[.*?\]', item],
            ['".*?"', string],
            ['#.*?$', comments],
        ]

        self.editArea = Text(
            self,
            background=background,
            foreground=normal,
            insertbackground=normal,
            relief=FLAT,
            borderwidth=30,
            font=font,
            height=35,
            width=104
        )

        font_for_tab = tkfont.Font(font=self.editArea['font'])
        tab_size = font_for_tab.measure('    ')
        self.editArea.config(tabs=tab_size)

        self.editArea.pack(
            fill=BOTH,
            expand=1
        )
        if content is None:
            self.editArea.insert('1.0', """<Region> {
    portrayal...
    requirements...
}

[Item] {
    portrayal...
    isStatic...
}

(Player) {
    portrayal...
}

start_position Region
final_position Region
            """)
        else:
            self.editArea.insert('1.0',content)

        self.editArea.bind('<KeyRelease>', self.changes)

        self.save_button = ttk.Button(self, text="Save", command=self.save_fiction)
        self.save_button.pack(pady=10)

        self.changes()

    def save_fiction(self):
        file_path = filedialog.asksaveasfilename(defaultextension=".game",
                                                 filetypes=[("IF_Game Files", "*.game"), ("All Files", "*.*")])
        if file_path:
            with open(file_path, "w") as file:
                file.write(self.editArea.get("1.0", "end-1c"))

    # Register Changes made to the Editor Content
    def changes(self, event=None):
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
        self.editArea.tag_configure("current_line", background="#363535")
        self.editArea.tag_raise("sel", "current_line")
        self._highlight_current_line()

    def _highlight_current_line(self, interval=100):
        if not self.editArea.winfo_exists():
            return
        self.editArea.tag_remove("current_line", "1.0", "end")
        self.editArea.tag_add("current_line", "insert linestart", "insert lineend+1c")
        self.after(100, self._highlight_current_line, 100)

    def search_re(self, pattern, text):
        matches = []

        text = text.splitlines()
        for i, line in enumerate(text):
            for match in re.finditer(pattern, line):
                matches.append((f"{i + 1}.{match.start()}", f"{i + 1}.{match.end()}"))

        return matches

    def rgb(self, rgb):
        return "#%02x%02x%02x" % rgb
