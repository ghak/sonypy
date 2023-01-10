import tkinter as tk
import cv2
from PIL import Image, ImageTk
import customtkinter

width, height = 1200, 600
cap = cv2.VideoCapture(1)
cap.set(cv2.CAP_PROP_FRAME_WIDTH, width)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, height)

root = customtkinter.CTk()
#root.bind('<Escape>', lambda e: root.quit())
lmain = customtkinter.CTkLabel(master=root, text="")
lmain.pack()
#frame = cv2.imread('/home/hakim/Desktop/AnalogDevices.jpg', 0)
def show_frame():
        _, frame = cap.read()
        frame = cv2.flip(frame, 1)
        cv2image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGBA)
        img = Image.fromarray(cv2image)
        ctkimgtk = customtkinter.CTkImage(img, size=(width, height))
        lmain.configure(image=ctkimgtk)
        lmain.after(10, show_frame)


show_frame()
root.mainloop()