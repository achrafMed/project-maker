from tkinter.ttk import *
from tkinter import messagebox
import sys


def close(root, func):
    def on_close():
        if messagebox.askokcancel("save", "Save changes?"):
            func()
    root.protocol("WM_DELETE_WINDOW", on_close)