import tkinter as tk
from tkinter import ttk,filedialog
import os

from gameFrame import GamePlayFrame


class App:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Interactive Fiction Creator")

        window_width = 800
        window_height = 600
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()
        x = (screen_width - window_width) // 2
        y = (screen_height - window_height) // 2
        self.root.geometry(f"{window_width}x{window_height}+{x}+{y}")

        self.navbar = tk.Menu(self.root)
        self.root.config(menu=self.navbar)
        self.navbar.add_command(label="Start", command=self.show_start_frame)
        self.navbar.add_command(label="Create Fiction", command=self.show_fiction_frame)
        self.navbar.add_command(label="Library", command=self.show_library_frame)

        self.start_frame = ttk.Frame(self.root)
        self.start_frame.pack()

        self.fiction_frame = ttk.Frame(self.root)

        self.load_library()

        self.text_area = tk.Text(self.fiction_frame, wrap=tk.WORD, width=100, height=30)
        self.text_area.pack(pady=10)

        self.fiction_type = tk.StringVar()
        self.fiction_type.set("game")

        self.game_radio = ttk.Radiobutton(self.fiction_frame, text="Game", variable=self.fiction_type, value="game",
                                          command=self.on_game_selected)
        self.game_radio.pack()

        self.movement_radio = ttk.Radiobutton(self.fiction_frame, text="Movement", variable=self.fiction_type,
                                              value="movement", command=self.on_movement_selected)
        self.movement_radio.pack()

        self.save_button = ttk.Button(self.fiction_frame, text="Save", command=self.save_fiction)
        self.save_button.pack(pady=10)

        self.play_button = ttk.Button(self.library_frame, text="Play", command=self.show_play_frame)
        self.play_button.pack(pady=10)

        self.show_start_frame()

        self.root.mainloop()

    def show_play_frame(self):
        selected_game = self.games_listbox.get(tk.ACTIVE)
        if selected_game:
            with open(selected_game, "r") as file:
                content = file.read()
            self.library_frame.pack_forget()
            self.play_frame = GamePlayFrame(self.root, content)
            self.play_frame.pack()

    def show_start_frame(self):
        self.fiction_frame.pack_forget()
        self.library_frame.pack_forget()
        self.start_frame.pack()

    def show_fiction_frame(self):
        self.start_frame.pack_forget()
        self.library_frame.pack_forget()
        self.fiction_frame.pack()
        self.on_game_selected()
        self.load_games()

    def show_library_frame(self):
        self.start_frame.pack_forget()
        self.fiction_frame.pack_forget()
        self.library_frame.pack()

    def save_fiction(self):
        file_path = filedialog.asksaveasfilename(defaultextension=".game",
                                                 filetypes=[("IF_Game Files", "*.game"), ("All Files", "*.*")])
        if file_path:
            with open(file_path, "w") as file:
                file.write(self.text_area.get("1.0", "end-1c"))

    def on_movement_selected(self):
        if self.fiction_type.get() == "movement":
            self.text_area.delete("1.0", "end")
            self.text_area.insert("1.0", "begin\n\nend\n")

    def on_game_selected(self):
        if self.fiction_type.get() == "game":
            self.text_area.delete("1.0", "end")
            self.text_area.insert("1.0",
                                  "(Region) { description ...}\n[Object] { description ...}\nPlayer { "
                                  "properties...}\nstart_position [Region]\n"
                                  "final_position [Region]")

    def load_library(self):
        self.library_frame = ttk.Frame(self.root)

        self.games_listbox = tk.Listbox(self.library_frame, selectmode=tk.SINGLE)
        self.games_listbox.pack(padx=10, pady=10)

        self.load_games()

        self.load_button = ttk.Button(self.library_frame, text="Load", command=self.load_selected_game)
        self.load_button.pack(pady=10)

    def load_games(self):
        saved_files = [f for f in os.listdir() if f.endswith(".game")]
        self.games_listbox.delete(0, tk.END)
        for saved_file in saved_files:
            self.games_listbox.insert(tk.END, saved_file)

    def load_selected_game(self):
        selected_game = self.games_listbox.get(tk.ACTIVE)
        if selected_game:
            with open(selected_game, "r") as file:
                content = file.read()
                self.text_area.delete("1.0", tk.END)
                self.text_area.insert("1.0", content)
                self.show_fiction_frame()