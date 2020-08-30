import sys, inspect
import tkinter.ttk


def print_classes():
    a = inspect.getmembers(sys.modules[tkinter.ttk.__name__])
   

    widgets = [e for e in a if inspect.isclass(e[1])]
    print(widgets)
print_classes()