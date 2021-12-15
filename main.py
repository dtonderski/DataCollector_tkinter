from tkinter import Tk, Label, Button, DISABLED, Entry, N, S, E, W
import tkinter as tk
from PIL import ImageTk, Image
from matplotlib import pyplot as plt
import numpy as np
import cv2
import os


class DataConfig:
    def __init__(self, rng_seed=None):
        self.max_height = 500
        self.max_shift = 100
        self.load_types = ["No load", "Pallet", "Pallet with barrels"]
        self.lighting_types = ["Daylight", "Artificial", "Flashlight"]
        self.background_objects = ["Obj1", "Obj2", "Obj3", "Obj4", "Obj5", "Obj6", "Obj7", "Obj8", "Obj9", "Obj10"]
        self.images_per_class_and_lighting = 20
        if rng_seed is None:
            self.rng_seed = np.random.default_rng().integers(1000)
        else:
            self.rng_seed = rng_seed
        self.rng = np.random.default_rng(self.rng_seed)

        self.shifts = self.rng.uniform(-self.max_shift, self.max_shift, self.n_images())
        self.heights = self.rng.uniform(0, self.max_height, self.n_images())

    def n_images(self):
        return len(self.load_types) * len(self.lighting_types) * self.images_per_class_and_lighting

class Layout:
    def __init__(self, master):
        self.master = master
        self.configure_grid()
        self.data_folder = "data"
        self.undo_folder = f"{self.data_folder}/undo"
        self.image_name_template = f"{self.data_folder}/{'{i}'}.jpg"
        self.undo_name_template = f"{self.undo_folder}/{'{i}'}.jpg"
        self.init_folders()

        self.current_image_index = 0
        self.current_image = None
        self.n_images = 12
        self.image_photo, self.image_frame, self.image_label = None, None, None
        self.init_image()

        self.cap = cv2.VideoCapture(0)
        self.camera_photo, self.camera_frame, self.camera_label = None, None, None
        self.init_camera()

        self.data_config = DataConfig()
        self.template_frame, self.template_label = None, None
        self.init_template()

        self.button_layout, self.back_button, self.forward_button, self.save_button, self.delete_button, \
        self.undo_button = self.init_buttons()

    def init_folders(self):
        if not os.path.exists(self.data_folder):
            os.mkdir(self.data_folder)
        if not os.path.exists(self.undo_folder):
            os.mkdir(self.undo_folder)

    def init_image(self):
        self.image_frame = tk.LabelFrame(self.master, text="Frame!")
        self.image_frame.grid(row=0, column=0, columnspan=1, sticky=N + S + E + W, padx=0, pady=0)
        self.image_label = Label(self.image_frame)
        self.update_image()
        self.image_frame.pack_propagate(False)

    def update_image(self):
        self.image_frame.configure(text=f"Image {self.current_image_index} / {self.n_images - 1}")
        self.image_label.destroy()

        if not os.path.exists(self.image_name_template.format(i=self.current_image_index)):
            return

        self.current_image = Image.open(self.image_name_template.format(i=self.current_image_index))
        self.image_photo = ImageTk.PhotoImage(self.current_image)

        self.image_label = Label(self.image_frame)
        self.image_label.image = self.image_photo
        self.image_label.pack(expand=True)
        self.image_label.bind('<Configure>', self.resize_image)

    def init_camera(self):
        self.camera_frame = tk.LabelFrame(self.master, text="Camera")
        self.camera_frame.grid(row=0, column=1, columnspan=1, sticky=N + S + E + W)
        self.camera_frame.pack_propagate(False)

        self.camera_label = Label(self.camera_frame)
        self.camera_label.pack(expand=True)
        self.camera_frame.update()

        self.update_camera()

    def update_camera(self):
        cv2image = cv2.cvtColor(self.cap.read()[1], cv2.COLOR_BGR2RGB)
        img = Image.fromarray(cv2image)
        resized_image = self.fit_image_to_frame(self.camera_frame, img)
        self.camera_photo = ImageTk.PhotoImage(image=resized_image)
        self.camera_label.configure(image=self.camera_photo)
        self.master.after(20, self.update_camera)

    def resize_image(self, event):
        image = self.current_image
        resized_image = self.fit_image_to_frame(self.image_frame, image)

        self.image_photo = ImageTk.PhotoImage(resized_image)
        self.image_label.configure(image=self.image_photo)

    def fit_image_to_frame(self, frame, image):
        frame_width = frame.winfo_width()
        frame_height = frame.winfo_height()
        frame_aspect_ratio = frame_width / frame_height

        image_width = image.size[0]
        image_height = image.size[1]
        image_aspect_ratio = image_width / image_height

        resized_image = image
        if image_width > frame_width or image_height > frame_height:
            if image_aspect_ratio > frame_aspect_ratio:
                resized_image = image.resize((frame_width, int(frame_width / image_aspect_ratio)))
            else:
                resized_image = image.resize((int(frame_height * image_aspect_ratio), frame_height))

        return resized_image

    def init_template(self):
        self.template_frame = tk.LabelFrame(self.master, text="Frame!")
        self.template_frame.grid(row=0, column=2, columnspan=1, sticky=N + S + E + W, padx=0, pady=0)
        self.template_label = Label(self.template_frame)
        # self.update_template()
        self.template_frame.pack_propagate(False)

    def init_buttons(self):
        button_layout = tk.LabelFrame(self.master)
        button_layout.grid(row=1, column=0, columnspan=3, sticky=N + S + E + W)
        button_layout.grid_columnconfigure(0, weight=1)
        button_layout.grid_columnconfigure(1, weight=1)
        button_layout.grid_columnconfigure(2, weight=1)
        button_layout.grid_columnconfigure(3, weight=1)
        button_layout.grid_columnconfigure(4, weight=1)
        button_layout.grid_columnconfigure(5, weight=1)

        button_layout.grid_rowconfigure(0, weight=1)
        button_layout.grid_rowconfigure(1, weight=1)

        forward_button = Button(button_layout, text="Next", command=self.forward)
        back_button = Button(button_layout, text="Back", command=self.back, state="disabled")
        save_button = Button(button_layout, text="Save", command=self.save)
        delete_button = Button(button_layout, text="Delete", command=self.delete)
        undo_button = Button(button_layout, text="Undo delete", command=self.undo)

        forward_button.grid(row=0, column=3, columnspan=3, sticky=N + S + E + W)
        back_button.grid(row=0, column=0, columnspan=3, sticky=N + S + E + W)
        save_button.grid(row=1, column=0, columnspan=2, sticky="nsew")
        delete_button.grid(row=1, column=2, columnspan=2, sticky="nsew")
        undo_button.grid(row=1, column=4, columnspan=2, sticky="nsew")
        return button_layout, back_button, forward_button, save_button, delete_button, undo_button

    def forward(self):
        self.current_image_index += 1
        self.update_buttons()
        self.update_image()

    def back(self):
        self.current_image_index -= 1
        self.update_buttons()
        self.update_image()

    def save(self):
        cv2image = self.cap.read()[1]
        cv2.imwrite(self.image_name_template.format(i=self.current_image_index), cv2image)
        self.update_image()

    def delete(self):
        current_filepath = self.image_name_template.format(i=self.current_image_index)
        undo_filepath = self.undo_name_template.format(i=self.current_image_index)
        if os.path.exists(current_filepath):
            os.replace(current_filepath, undo_filepath)
        self.update_image()

    def undo(self):
        current_filepath = self.image_name_template.format(i=self.current_image_index)
        undo_filepath = self.undo_name_template.format(i=self.current_image_index)
        if os.path.exists(undo_filepath):
            os.replace(undo_filepath, current_filepath)
        self.update_image()

    def update_buttons(self):
        self.forward_button["state"] = "active"
        self.back_button["state"] = "active"

        if self.current_image_index == 0:
            self.back_button["state"] = "disabled"
        elif self.current_image_index == self.n_images - 1:
            self.forward_button["state"] = "disabled"

    def configure_grid(self):
        self.master.grid_columnconfigure(0, weight=1)
        self.master.grid_columnconfigure(1, weight=1)
        self.master.grid_columnconfigure(2, weight=1)
        self.master.grid_rowconfigure(0, weight=4)
        self.master.grid_rowconfigure(1, weight=1)


root = Tk()
root.geometry("400x800")
a = Layout(root)

root.mainloop()
