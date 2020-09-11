from tkinter.ttk import *




def getProperties(widget):
    return list(widget.keys())


def changeValue(widget):
    return 0

def renderProperties(widget, parent):
    attributes = getProperties(widget)
    i = 0
    for attr in attributes:
        attrButton = Button(parent, text=attr)
        attrButton['command'] = lambda e=attrButton: changeValue(attrButton)
        attrButton.grid(row=i, column=0)
        attrValue = Label(parent, text=widget[attr])
        attrValue.grid(row=i, column=1)
        i+=1



