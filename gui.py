# -*- coding: utf-8 -*-
"""
Created on Mon Jan  10 08:51:49 2023

@author: ghak
"""
import tkinter
from camera import Camera
import customtkinter
import os
from PIL import Image
import cv2


class App(customtkinter.CTk):
    def __init__(self, interface='eth0'):
        super().__init__()
        self.image_shape = (800, 600)
        
        self.init_camera(interface)
        
        self.protocol("WM_DELETE_WINDOW", self.on_closing)
        self.title("SonyPy")
        self.geometry("1024x768")
        
        # set grid layout 1x2
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)

        # create navigation frame
        self.navigation_frame = customtkinter.CTkFrame(self, corner_radius=0)
        self.navigation_frame.grid(row=0, column=0, sticky="nsew")
        self.navigation_frame.grid_rowconfigure(4, weight=1)

        #self.large_test_image = customtkinter.CTkImage(Image.open('/home/hakim/Desktop/AnalogDevices.jpg'), size=(500, 150))
        self.init_control_panel()
        self.init_main_frame()
        self.init_preview_frame()
    
    def init_camera(self, interface):
        self.a6000 = Camera(interface=interface)
        
    def init_control_panel(self):
        self.control_panel = customtkinter.CTkLabel(self.navigation_frame, text="Control Panel",
                                                             compound="left", font=customtkinter.CTkFont(size=15, weight="bold"))
        self.control_panel.grid(row=0, column=0, padx=20, pady=20)

        self.capture_button = customtkinter.CTkButton(self.control_panel, corner_radius=0, height=40, border_spacing=10, text="Button 1",
                                                   fg_color="transparent", text_color=("gray10", "gray90"), hover_color=("gray70", "gray30"),
                                                   anchor="w", command=self.button1_event)
        self.capture_button.grid(row=10, column=0, sticky="ew")

        
        """self.slider = customtkinter.CTkSlider(self.control_panel, number_of_steps=10,
                                              command=self.slider_event)
        
        self.slider.grid(row=4, column=0, padx=20, pady=20, sticky="ew")

        self.option_menu = customtkinter.CTkOptionMenu(self.control_panel, values=["opt1", "opt2", "opt3"],
                                                                command=self.option_menu_event)
        self.option_menu.grid(row=5, column=0, padx=20, pady=20, sticky="ew")"""
    
    
    def init_main_frame(self):
        self.home_frame = customtkinter.CTkFrame(self, corner_radius=0, fg_color="transparent")
        self.home_frame.grid_columnconfigure(0, weight=1)
        self.home_frame.grid(row=0, column=1, sticky="nsew")
        
        self.preview = customtkinter.CTkLabel(self.home_frame, text="")
        self.preview.grid(row=0, column=0, padx=20, pady=10)
        
    def init_preview_frame(self):
        self.cap = cv2.VideoCapture(self.a6000.startLiveView('M'))
        self.image_shape  = (self.cap.get(cv2.CAP_PROP_FRAME_WIDTH),self.cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
        self.show_frame()
    
    def on_closing(self):
        print("closing")
        self.cap.release()
        self.a6000.stopLiveView()
        self.a6000.stop_remote_mode()
        self.destroy()
        
    def show_frame(self):
        try:
            _, frame = self.cap.read()
            cv2image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGBA)
            img = Image.fromarray(cv2image)
            ctkimgtk = customtkinter.CTkImage(img, size=self.image_shape)
            self.preview.configure(image=ctkimgtk)
            self.preview.after(10, self.show_frame)
        except Exception as e:
            print(e)

    def button1_event(self):
        print("Button 1")

    def button2_event(self):
        print("Button 2")

    def button3_event(self):
        print("Button 3")

    def option_menu_event(self, opt):
        print(opt)
    
    def slider_event(self, value):
        print(value)
        



