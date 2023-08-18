import tkinter as tk
from tkinter import ttk, messagebox
import os

from gameFrame import GamePlayFrame
from pictureCreatorFrame import PictureCreatorFrame
from codeEditorFrame import CodeEditorFrame


class App:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Interactive Fiction Creator")
        self.play_frame = ttk.Frame(self.root)
        self.picture_creator_frame = ttk.Frame(self.root)

        window_width = 1200
        window_height = 985
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()
        x = (screen_width - window_width) // 2
        y = (screen_height - window_height) // 2
        self.root.geometry(f"{window_width}x{window_height}+{x}+{y - 50}")

        self.navbar = tk.Menu(self.root)
        self.root.config(menu=self.navbar)
        self.navbar.add_command(label="Start", command=self.show_start_frame)
        self.navbar.add_command(label="Create Fiction", command=lambda: self.show_fiction_frame(None))
        self.navbar.add_command(label="Library", command=self.show_library_frame)

        self.start_frame = ttk.Frame(self.root)
        self.start_frame.pack()

        self.fiction_frame = ttk.Frame(self.root)

        self.load_library()

        self.text_area = tk.Text(self.fiction_frame, wrap=tk.WORD, width=90, height=50)
        self.text_area.pack(pady=10)

        self.fiction_type = tk.StringVar()
        self.fiction_type.set("game")


        self.play_button = ttk.Button(self.library_frame, text="Play", command=self.show_play_frame)
        self.play_button.pack(pady=10)

        self.picture_creator_button = ttk.Button(self.library_frame, text="Picture creator",
                                                 command=self.show_picture_creator_frame)
        self.picture_creator_button.pack(pady=10)

        self.with_images_var = tk.BooleanVar()
        self.with_images_checkbox = ttk.Checkbutton(self.library_frame, text="With Images",
                                                    variable=self.with_images_var)
        self.with_images_checkbox.pack(pady=10)

        self.show_start_frame()

        self.root.mainloop()

    def show_play_frame(self):
        self.fiction_frame.pack_forget()
        self.library_frame.pack_forget()
        self.start_frame.pack_forget()
        self.picture_creator_frame.pack_forget()

        selected_game = self.games_listbox.get(tk.ACTIVE)
        if selected_game:
            games_directory = "games/" + selected_game + "/" + selected_game
            with open(games_directory, "r") as file:
                content = file.read()
            self.library_frame.pack_forget()
            with_images = self.with_images_var.get()
            self.play_frame = GamePlayFrame(self.root, selected_game, content, with_images)
            self.play_frame.pack()

    def show_start_frame(self):
        self.fiction_frame.pack_forget()
        self.library_frame.pack_forget()
        self.play_frame.pack_forget()
        self.picture_creator_frame.pack_forget()
        self.start_frame.pack()

    def show_fiction_frame(self,content=None):
        self.fiction_frame.pack_forget()
        self.start_frame.pack_forget()
        self.library_frame.pack_forget()
        self.play_frame.pack_forget()
        self.picture_creator_frame.pack_forget()
        self.on_game_selected(content)
        self.load_games()

    def show_library_frame(self):
        self.start_frame.pack_forget()
        self.play_frame.pack_forget()
        self.fiction_frame.pack_forget()
        self.picture_creator_frame.pack_forget()
        self.library_frame.pack()


    def on_game_selected(self,content=None):
        self.fiction_frame = CodeEditorFrame(self.root,content)
        self.fiction_frame.pack()
        if content is None:
            messagebox.showinfo("Information", "Steps when saving your game: \n 1) Create a new folder with the same name "
                                               "as your game (\"simplegame.game\") inside the games folder \n 2) Save "
                                               "your game inside the folder you just created \n ("
                                               "\"games/simplegame.game/simplegame.game\") should be the path to your "
                                               "game code")

    def load_library(self):
        self.library_frame = ttk.Frame(self.root)

        self.games_listbox = tk.Listbox(self.library_frame, selectmode=tk.SINGLE)
        self.games_listbox.pack(padx=10, pady=10)

        self.load_games()

        self.load_button = ttk.Button(self.library_frame, text="Load code", command=self.load_selected_game)
        self.load_button.pack(pady=10)

    def show_picture_creator_frame(self):
        self.fiction_frame.pack_forget()
        self.library_frame.pack_forget()
        self.start_frame.pack_forget()
        self.play_frame.pack_forget()

        selected_game = self.games_listbox.get(tk.ACTIVE)
        if selected_game:
            games_directory = "games/" + selected_game
            self.library_frame.pack_forget()
            self.picture_creator_frame = PictureCreatorFrame(self.root, games_directory, selected_game)
            self.picture_creator_frame.pack()

    def load_games(self):
        games_directory = "games"
        saved_files = [f for f in os.listdir(os.path.join(os.getcwd(), games_directory)) if f.endswith(".game")]
        self.games_listbox.delete(0, tk.END)
        for saved_file in saved_files:
            self.games_listbox.insert(tk.END, saved_file)

    def load_selected_game(self):
        selected_game = self.games_listbox.get(tk.ACTIVE)
        if selected_game:
            games_directory = "games/" + selected_game
            game_path = os.path.join(games_directory, selected_game)
            with open(game_path, "r") as file:
                content = file.read()
                self.show_fiction_frame(content)
