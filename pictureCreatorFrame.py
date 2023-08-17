import tkinter as tk
from tkinter import ttk
from functools import partial #zarad okidanja samo kada se klikne dugme


from gameInterpeter import parse_dsl
from PIL import ImageTk
from PIL import Image

from diffusers import StableDiffusionPipeline
import os

SDV5_MODEL_PATH = os.getenv('SDV5_MODEL_PATH')


pipeline = StableDiffusionPipeline.from_pretrained(SDV5_MODEL_PATH, safety_checker=None,
                                                   requires_safety_checker=False)
pipeline.enable_sequential_cpu_offload()


class PictureCreatorFrame(ttk.Frame):
    def __init__(self, parent, games_directory, selected_game):
        super().__init__(parent)

        self.gameWorld = parse_dsl("gameWorldDSL.tx", games_directory+"/"+selected_game)

        self.text_area = tk.Text(self, wrap=tk.WORD, width=80, height=3)
        self.text_area.insert("1.0", self.gameWorld.regions[0].print_self_for_stable())
        self.text_area.grid(row=0, column=0, columnspan=4)

        self.generate_button = tk.Button(self, text="Generate", command=partial(self.generate_image, games_directory))
        self.generate_button.grid(row=1, column=0, columnspan=2,padx=10, pady=10)

        self.image_label0 = tk.Label(self, width=512, height=256)
        self.image_label1 = tk.Label(self, width=512, height=256)
        self.image_label2 = tk.Label(self, width=512, height=256)
        self.image_label3 = tk.Label(self, width=512, height=256)

        self.image_label0.grid(row=2, column=0)
        self.image_label1.grid(row=2, column=1)
        self.image_label2.grid(row=4, column=0)
        self.image_label3.grid(row=4, column=1)

        if os.path.isfile(games_directory+"/generatedImg0.png"):
            img0 = Image.open(games_directory+"/generatedImg0.png")
            img1 = Image.open(games_directory+"/generatedImg1.png")
            img2 = Image.open(games_directory+"/generatedImg2.png")
            img3 = Image.open(games_directory+"/generatedImg3.png")

            img0 = img0.resize((512, 256))
            img1 = img1.resize((512, 256))
            img2 = img2.resize((512, 256))
            img3 = img3.resize((512, 256))

        else:
            img0 = Image.open("games/noImg.png")
            img1 = Image.open("games/noImg.png")
            img2 = Image.open("games/noImg.png")
            img3 = Image.open("games/noImg.png")

            img0 = img0.resize((512, 256))
            img1 = img1.resize((512, 256))
            img2 = img2.resize((512, 256))
            img3 = img3.resize((512, 256))

        self.img0 = ImageTk.PhotoImage(img0)
        self.img1 = ImageTk.PhotoImage(img1)
        self.img2 = ImageTk.PhotoImage(img2)
        self.img3 = ImageTk.PhotoImage(img3)
        self.image_label0.config(image=self.img0)
        self.image_label1.config(image=self.img1)
        self.image_label2.config(image=self.img2)
        self.image_label3.config(image=self.img3)

        self.radio_var = tk.StringVar(value="Option 1")

        self.radio_button0 = tk.Radiobutton(self, text="Option 1", variable=self.radio_var, value="Option 1")
        self.radio_button1 = tk.Radiobutton(self, text="Option 2", variable=self.radio_var, value="Option 2")
        self.radio_button2 = tk.Radiobutton(self, text="Option 3", variable=self.radio_var, value="Option 3")
        self.radio_button3 = tk.Radiobutton(self, text="Option 4", variable=self.radio_var, value="Option 4")

        self.radio_button0.grid(row=3, column=0, padx=10, pady=10)
        self.radio_button1.grid(row=3, column=1, padx=10, pady=10)
        self.radio_button2.grid(row=5, column=0, padx=10, pady=10)
        self.radio_button3.grid(row=5, column=1, padx=10, pady=10)

    def generate_image(self,games_directory):
        img0 = pipeline(self.text_area.get("1.0", "end-1c").lower(),width=512, height=256).images[0]
        img1 = pipeline(self.text_area.get("1.0", "end-1c").lower(),width=512, height=256).images[0]
        img2 = pipeline(self.text_area.get("1.0", "end-1c").lower(),width=512, height=256).images[0]
        img3 = pipeline(self.text_area.get("1.0", "end-1c").lower(),width=512, height=256).images[0]
        img0.save(games_directory+'/generatedImg0.png')
        img1.save(games_directory+'/generatedImg1.png')
        img2.save(games_directory+'/generatedImg2.png')
        img3.save(games_directory+'/generatedImg3.png')
        self.img0 = ImageTk.PhotoImage(img0)
        self.img1 = ImageTk.PhotoImage(img1)
        self.img2 = ImageTk.PhotoImage(img2)
        self.img3 = ImageTk.PhotoImage(img3)
        self.image_label0.config(image=self.img0)
        self.image_label1.config(image=self.img1)
        self.image_label2.config(image=self.img2)
        self.image_label3.config(image=self.img3)