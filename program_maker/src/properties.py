from tkinter import *
from tkinter.ttk import *

root = ''


def getProperties(widget):
    return list(widget.keys())


def changeValue(valueLabel, index, widget):
    global root
    t = valueLabel['text']
    valueLabel.destroy()
    valueEntry = Entry(root.propertiesParent)
    text = StringVar()
    valueEntry['textvariable'] = text
    text.set(t)
    valueEntry.bind("<Return>", lambda v, i= index, w=widget: changeState(v,i,w))
    valueEntry.grid(row=index, column=1)

def changeState(event,i, widget):
    valueEntry = event.widget
    properties = getProperties(widget)
    widget[properties[i]] = valueEntry.get()
    valueEntry.destroy()
    valueLabel = Label(root.propertiesParent, text=widget['text'])
    valueLabel.grid(row=i, column=1)

def renderProperties(widget, self):
    global root; root = self
    attributes = getProperties(widget)
    self.propertiesParent.destroy()
    self.propertiesParent = Frame(self.widgetContainer)
    self.propertiesParent.pack(side='bottom')
    parent = self.propertiesParent
    i = 0
    for i,attr in enumerate(attributes):
        attrValue = Label(parent, text=widget[attr])
        attrValue.grid(row=i, column=1)
        attrButton = Button(parent, text=attr)
        attrButton['command'] = lambda e=attrValue, index=i, w=widget: changeValue(e, index, w)
        attrButton.grid(row=i, column=0)
        

