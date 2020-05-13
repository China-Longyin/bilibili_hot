#!/usr/bin/env python
# -*- coding: utf-8 -*-
# 作者：龙.吟


import tkinter

from tkinter import filedialog


def select_path():
    root = tkinter.Tk()

    root.withdraw()

    file_path = filedialog.askopenfilename()

    return file_path
