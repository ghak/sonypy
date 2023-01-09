#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Jan  9 14:59:49 2023

@author: ghak
"""

from camera import Camera
import cv2

def preview_camera(mirror=False, url=0):
    cam = cv2.VideoCapture(url)
    while True:
        ret, img = cam.read()
        if mirror: 
            img = cv2.flip(img, 1)
        if not ret:
            continue
        cv2.imshow('my webcam', img)
        if cv2.waitKey(1) == 27: 
            break  # esc to quit
    cv2.destroyAllWindows()


def main():
    a6000 = Camera(interface='wlp4s0f0')
    print(a6000.services)
    a6000.start_remote_mode()
    #a6000.getSupportedLiveViewSize()
    url = a6000.startLiveView('L')
    preview_camera(mirror=False, url=url)


if __name__ == '__main__':
    main()
