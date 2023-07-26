import tkinter as tk
from tkinter import ttk
from gameInterpeter import parse_dsl
from PIL import ImageTk

from diffusers import StableDiffusionPipeline
import os

SDV5_MODEL_PATH = os.getenv('SDV5_MODEL_PATH')

possible_commands = [
    "move N",
    "move S",
    "move W",
    "move E",
    "drop <item>",
    "open <item>",
    "take <item>",
    "use <item>"
]

# Help command message
help_message = "Possible commands:\n" + "\n".join(possible_commands)
pipeline = StableDiffusionPipeline.from_pretrained(SDV5_MODEL_PATH, safety_checker=None,
                                                   requires_safety_checker=False)
pipeline.enable_sequential_cpu_offload()


class GamePlayFrame(ttk.Frame):
    def __init__(self, parent, game_title, game_content, with_images):
        super().__init__(parent)


        self.gameWorld = parse_dsl("gameWorldDSL.tx", game_title)

        frame_title_label = ttk.Label(self, text=game_title[:-5], font=("Arial", 14, "bold"))
        frame_title_label.pack(pady=10)

        self.text_area = tk.Text(self, wrap=tk.WORD, width=80, height=20)
        self.text_area.pack(pady=10)
        self.text_area.insert("1.0", self.gameWorld.regions[0].print_self())  # Replace with parsed text

        self.input_label = ttk.Label(self, text="Type your commands:")
        self.input_label.pack(pady=5)
        self.input_entry = ttk.Entry(self, width=50)
        self.input_entry.pack(pady=5)
        self.input_entry.bind("<Return>", lambda event: self.process_user_input(event, with_images))

        if with_images:
            self.image_label = tk.Label(self, width=512, height=512)
            self.image_label.pack()
            self.generate_image(self.gameWorld.regions[0].print_self_for_stable())  # Call your image generation function here

    def generate_image(self, prompt):
        image = pipeline(prompt.lower(),width=512, height=512).images[0]
        image.save('generatedImg.png')
        self.img = ImageTk.PhotoImage(image)
        self.image_label['image'] = self.img

    def display_help(self):
        self.text_area.insert("end", "\n\n" + help_message + "\n\n")

    def process_user_input(self, event, with_images):
        user_input = self.input_entry.get().strip()
        self.text_area.insert("end", '\n' + user_input)
        self.input_entry.delete(0, tk.END)
        the_end = False

        if self.gameWorld.player.position == self.gameWorld.final_position:
            possible_moves = ["move N", "move E", "move S", "move W"]
            for door in self.gameWorld.final_position.doors:
                possible_move = "move " + door
                possible_moves.remove(possible_move)
            if user_input in possible_moves:
                self.text_area.delete("1.0", tk.END)
                self.text_area.insert("1.0", "THE END")
                the_end = True
                if with_images:
                    self.img = ImageTk.PhotoImage(file="theEnd.jpg")
                    self.image_label['image'] = self.img

        if user_input in ["move N", "move E", "move S", "move W"] and not the_end:
            direction = user_input[-1]
            text,moved = self.gameWorld.player.move(direction, self.gameWorld)
            self.text_area.insert("end", '\n' + text)
            self.text_area.insert("end", '\n' + self.gameWorld.player.print_self())
            if with_images:
                if moved:
                    self.generate_image(self.gameWorld.player.position.print_self_for_stable())
        elif "take" in user_input and not the_end:
            item = user_input[5:]
            text = self.gameWorld.player.take(item, self.gameWorld)
            self.text_area.insert("end", '\n' + text)
            self.text_area.insert("end", '\n' + self.gameWorld.player.print_self())
        elif "drop" in user_input and not the_end:
            item = user_input[5:]
            text = self.gameWorld.player.drop(item, self.gameWorld)
            self.text_area.insert("end", '\n' + text)
            self.text_area.insert("end", '\n' + self.gameWorld.player.print_self())
        elif "use" in user_input and not the_end:
            item = user_input[4:]
            text = self.gameWorld.player.use(item, self.gameWorld)
            self.text_area.insert("end", '\n' + text)
            self.text_area.insert("end", '\n' + self.gameWorld.player.print_self())
        elif "open" in user_input and not the_end:
            item = user_input[5:]
            text = self.gameWorld.player.open(item, self.gameWorld)
            self.text_area.insert("end", '\n' + text)
            self.text_area.insert("end", '\n' + self.gameWorld.player.print_self())
        elif "help" in user_input and not the_end:
            self.display_help()
        elif not the_end:
            self.text_area.insert("end", " <--> Invalid command. Type help for possible commands")
