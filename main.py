from tkinter import Tk, Label, Button, DISABLED, Entry, N, S, E, W
import tkinter as tk
from PIL import ImageTk, Image
from matplotlib import pyplot as plt
import cv2


class Layout():
    def __init__(self, master):
        self.master = master
        self.image_list = [Image.open(f'data/{i}.jpg') for i in range(1, 4)]
        self.current_image = 0
        self.n_images = len(self.image_list)
        self.image_photo, self.image_frame, self.image_label = None, None, None
        self.init_image_frame()
        self.back_button, self.forward_button = self.init_buttons()
        self.configure_grid()

    def init_image_frame(self):
        self.image_frame = tk.LabelFrame(self.master, text="Frame!")
        self.image_frame.grid(row=0, column=0, columnspan=1, sticky=N + S + E + W, padx=0, pady=0)
        self.image_label = Label(self.image_frame)
        self.update_image()
        self.image_frame.pack_propagate(False)

    def init_camera_frame(self):
        self.camera_frame = tk.LabelFrame(self.master, text="Camera!")
        self.camera_frame.grid(row=0, column=0, columnspan=1, sticky=N + S + E + W)
        self.camera_label = Label(self.camera_frame)
        self.update_camera()
        self.camera_frame.pack_propagate(False)

    def init_buttons(self):
        forward_button = Button(self.master, text="Next", command=self.forward)
        back_button = Button(self.master, text="Back", command=self.back, state="disabled")

        forward_button.grid(row=1, column=1, sticky=N + S + E + W)
        back_button.grid(row=1, column=0, sticky=N + S + E + W)

        return back_button, forward_button

    def configure_grid(self):
        self.master.grid_columnconfigure(0, weight=1)
        self.master.grid_columnconfigure(1, weight=1)
        self.master.grid_rowconfigure(0, weight=4)
        self.master.grid_rowconfigure(1, weight=1)

    def forward(self):
        self.current_image += 1
        self.update_buttons()
        self.update_image()

    def back(self):
        self.current_image -= 1
        self.update_buttons()
        self.update_image()

    def update_image(self):
        self.image_label.destroy()

        image = self.image_list[self.current_image]

        self.image_photo = ImageTk.PhotoImage(image)
        self.image_label = Label(self.image_frame, image=self.image_photo)
        self.image_label.pack(expand=True)
        self.image_label.bind('<Configure>',
                              lambda event: self.resize(event, self.image_frame, self.image_label, image, "image"))
        self.image_label.configure(image=self.image_photo)

    def resize(self, event, frame, label, image, mode):
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
        if mode == "image":
            self.image_photo = ImageTk.PhotoImage(resized_image)
            label.configure(image=self.image_photo)
        elif mode == "camera":
            self.camera_photo = ImageTk.PhotoImage(resized_image)
            label.configure(image = self.camera_photo)

    def resize_image(self, event):

        image = self.image_list[self.current_image]

        frame_width = self.image_frame.winfo_width()
        frame_height = self.image_frame.winfo_height()
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

        self.image_photo = ImageTk.PhotoImage(resized_image)
        self.image_label.configure(image=self.image_photo)

    def update_buttons(self):
        self.forward_button["state"] = "active"
        self.back_button["state"] = "active"

        if self.current_image == 0:
            self.back_button["state"] = "disabled"
        elif self.current_image == self.n_images - 1:
            self.forward_button["state"] = "disabled"


root = Tk()
root.geometry("400x800")
Layout(root)
root.mainloop()
