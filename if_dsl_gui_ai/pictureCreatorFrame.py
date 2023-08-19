import tkinter as tk
from tkinter import ttk, messagebox
from functools import partial  # zarad okidanja samo kada se klikne dugme

from if_dsl_gui_ai.gameInterpeter import parse_dsl
from PIL import ImageTk
from PIL import Image

from diffusers import StableDiffusionPipeline
import os

try:
    SDV5_MODEL_PATH = os.getenv('SDV5_MODEL_PATH')
    pipeline = StableDiffusionPipeline.from_pretrained(SDV5_MODEL_PATH, safety_checker=None,
                                                   requires_safety_checker=False)
    print("Local version")
except:
    pipeline = StableDiffusionPipeline.from_pretrained("CompVis/stable-diffusion-v1-4", safety_checker=None,
                                                       requires_safety_checker=False, use_auth_token="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")
    print("Online version")

pipeline.enable_sequential_cpu_offload()


class PictureCreatorFrame(ttk.Frame):
    def __init__(self, parent, games_directory, selected_game):
        super().__init__(parent)
        self.default_img = Image.open("if_dsl_gui_ai/noImg.png")
        try:
            self.gameWorld = parse_dsl("gameWorldDSL.tx", selected_game)
        except:
            messagebox.showinfo("Information", "Game code is invalid. You need to verify it.")
            return

        self.counter = -1
        self.next_region_button = tk.Button(self, text="Next region", command=partial(self.generate_next_region, games_directory))
        self.next_region_button.grid(row=6, column=1, columnspan=2, padx=10, pady=10)

    def generate_next_region(self,games_directory):
        if self.counter < len(self.gameWorld.regions):
            self.counter = self.counter + 1
            if self.counter == len(self.gameWorld.regions):
                messagebox.showinfo("Information", "You have created pictures for your game.")
                self.pack_forget()
            else:

                self.next_region_button.grid_remove()
                self.region_name = self.gameWorld.regions[self.counter].name
                self.text_area = tk.Text(self, wrap=tk.WORD, width=80, height=3)
                self.text_area.insert("1.0", self.gameWorld.regions[self.counter].print_self_for_stable())
                self.text_area.grid(row=0, column=0, columnspan=4)

                self.generate_button = tk.Button(self, text="Generate",
                                                 command=partial(self.generate_image))
                self.generate_button.grid(row=1, column=0, columnspan=2, padx=10, pady=10)

                self.save_button = tk.Button(self, text="Pick",
                                             command=partial(self.save_image, games_directory))
                self.save_button.grid(row=6, column=0, columnspan=2, padx=10, pady=10)

                self.image_label0 = tk.Label(self, width=512, height=256)
                self.image_label1 = tk.Label(self, width=512, height=256)
                self.image_label2 = tk.Label(self, width=512, height=256)
                self.image_label3 = tk.Label(self, width=512, height=256)

                self.image_label0.grid(row=2, column=0)
                self.image_label1.grid(row=2, column=1)
                self.image_label2.grid(row=4, column=0)
                self.image_label3.grid(row=4, column=1)

                if not os.path.isfile(games_directory + "/" + self.region_name + ".png"):
                    self.img0_fromPipe = Image.open("if_dsl_gui_ai/noImg.png")
                    self.img1_fromPipe = Image.open("if_dsl_gui_ai/noImg.png")
                    self.img2_fromPipe = Image.open("if_dsl_gui_ai/noImg.png")
                    self.img3_fromPipe = Image.open("if_dsl_gui_ai/noImg.png")

                    img0 = self.img0_fromPipe.resize((512, 256))
                    img1 = self.img1_fromPipe.resize((512, 256))
                    img2 = self.img2_fromPipe.resize((512, 256))
                    img3 = self.img3_fromPipe.resize((512, 256))

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
                else:
                    messagebox.showinfo("Information", "You have already created pictures for your game. If you want "
                                                       "to change them remove all of them from the game directory "
                                                       "then try the picture creator once more.")

    def generate_image(self):
        self.img0_fromPipe = pipeline(self.text_area.get("1.0", "end-1c").lower(), width=512, height=256).images[0]
        self.img1_fromPipe = pipeline(self.text_area.get("1.0", "end-1c").lower(), width=512, height=256).images[0]
        self.img2_fromPipe = pipeline(self.text_area.get("1.0", "end-1c").lower(), width=512, height=256).images[0]
        self.img3_fromPipe = pipeline(self.text_area.get("1.0", "end-1c").lower(), width=512, height=256).images[0]

        self.img0 = ImageTk.PhotoImage(self.img0_fromPipe)
        self.img1 = ImageTk.PhotoImage(self.img1_fromPipe)
        self.img2 = ImageTk.PhotoImage(self.img2_fromPipe)
        self.img3 = ImageTk.PhotoImage(self.img3_fromPipe)
        self.image_label0.config(image=self.img0)
        self.image_label1.config(image=self.img1)
        self.image_label2.config(image=self.img2)
        self.image_label3.config(image=self.img3)

    def save_image(self, games_directory):
        if self.radio_var.get() == "Option 1":
            self.img0_fromPipe.save(games_directory + '/' + self.region_name + '.png')
        elif self.radio_var.get() == "Option 2":
            self.img1_fromPipe.save(games_directory + '/' + self.region_name + '.png')
        elif self.radio_var.get() == "Option 3":
            self.img2_fromPipe.save(games_directory + '/' + self.region_name + '.png')
        elif self.radio_var.get() == "Option 4":
            self.img3_fromPipe.save(games_directory + '/' + self.region_name + '.png')
        self.save_button.grid_remove()
        self.next_region_button.grid(row=6, column=1, columnspan=2, padx=10, pady=10)
