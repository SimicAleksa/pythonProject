import tkinter as tk
from tkinter import ttk

from gameInterpeter import parse_dsl


class GamePlayFrame(ttk.Frame):
    def __init__(self, parent, game_title,game_content):
        super().__init__(parent)

        # Parse the game_content here as needed
        self.gameWorld = parse_dsl("gameWorldDSL.tx",game_title)



        frame_title_label = ttk.Label(self, text=game_title[:-5], font=("Arial", 14, "bold"))
        frame_title_label.pack(pady=10)

        # Display the parsed text
        self.text_area = tk.Text(self, wrap=tk.WORD, width=80, height=20)
        self.text_area.pack(pady=10)
        self.text_area.insert("1.0", self.gameWorld.regions[0].print_self())  # Replace with parsed text

        # Display the image (replace the 'generate_image' function with your image generation code)
        self.image_label = ttk.Label(self, text="Image will appear here.")
        self.image_label.pack(pady=10)
        self.generate_image()  # Call your image generation function here

        # Input area for user interaction
        self.input_label = ttk.Label(self, text="Type your commands:")
        self.input_label.pack(pady=5)
        self.input_entry = ttk.Entry(self, width=50)
        self.input_entry.pack(pady=5)
        self.input_entry.bind("<Return>", self.process_user_input)

    def generate_image(self):
        # Replace this with your image generation code
        # For example, you can create a Canvas widget and draw the image using shapes and colors
        pass

    def process_user_input(self, event):
        while True:
            user_input = self.input_entry.get()
            self.text_area.insert("end", '\n' + user_input)
            self.input_entry.delete(0, tk.END)
            if self.gameWorld.player.properties["PositionProperties"] == self.gameWorld.final_position:
                self.text_area.delete("1.0", tk.END)
                self.text_area.insert("1.0", "THE END")

