import tkinter as tk
from PIL import Image, ImageTk

class Layout:
    def __init__(self, master):
        self.master = master
        self.rootgeometry()
        self.canvas = tk.Canvas(self.master)
        self.canvas.pack()
        self.background_image = Image.open('image_file.PNG')
        self.image_copy = self.background_image.copy()
        self.background = ImageTk.PhotoImage(self.background_image)
        self.loadbackground()


def loadbackground(self):
    self.label = tk.Label(self.canvas, image=self.background)
    self.label.pack(fill='both', expand='yes')


def rootgeometry(self):
    x = int(self.master.winfo_screenwidth() * 0.7)
    y = int(self.master.winfo_screenheight() * 0.7)
    z = str(x) + 'x' + str(y)
    self.master.geometry(z)


def resizeimage(self, event):
    image = self.image_copy.resize((self.master.winfo_width(), self.master.winfo_height()))
    self.image1 = ImageTk.PhotoImage(image)
    self.label.config(image=self.image1)


root = tk.Tk()
a = Layout(root)
root.mainloop()