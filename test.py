# Import required Libraries
from tkinter import *
from PIL import Image, ImageTk
import cv2

# Create an instance of TKinter Window or frame
win = Tk()

# Set the size of the window
win.geometry("700x350")
win.grid_columnconfigure(0, weight=1)
win.grid_columnconfigure(1, weight=1)
win.grid_rowconfigure(0, weight=4)
win.grid_rowconfigure(1, weight=1)

# Create a frame
frame = LabelFrame(win, text="Frame!")
frame.grid(row=0, column=0, columnspan=1, sticky=N + S + E + W, padx=0, pady=0)
frame.pack_propagate(False)

# Create a Label to capture the Video frames
label = Label(frame)
label.grid(row=0, column=0)
cap = cv2.VideoCapture(0)

frame.update()


# Define function to show frame
def show_frames():
    # Get the latest frame and convert into Image
    cv2image = cv2.cvtColor(cap.read()[1], cv2.COLOR_BGR2RGB)
    img = Image.fromarray(cv2image)
    # Convert image to PhotoImage

    frame_width = frame.winfo_width()
    frame_height = frame.winfo_height()
    frame_aspect_ratio = frame_width / frame_height

    image_width = img.size[0]
    image_height = img.size[1]
    image_aspect_ratio = image_width / image_height

    resized_image = img
    if image_width > frame_width or image_height > frame_height:
        if image_aspect_ratio > frame_aspect_ratio:
            resized_image = img.resize((frame_width, int(frame_width / image_aspect_ratio)))
        else:
            resized_image = img.resize((int(frame_height * image_aspect_ratio), frame_height))

    print(resized_image.size[0])
    imgtk = ImageTk.PhotoImage(image=resized_image)
    label.imgtk = imgtk
    label.configure(image=imgtk)

    # Repeat after an interval to capture continiously
    label.after(20, show_frames)

show_frames()

win.mainloop()
