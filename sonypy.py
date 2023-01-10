#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Jan  9 14:59:49 2023

@author: ghak
"""


from gui import App


def main():
    app = App(interface='wlp4s0f0')
    app.mainloop()


if __name__ == '__main__':
    main()
