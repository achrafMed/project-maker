from tkinter import *
from tkinter.ttk import *

root = ''
k = 0
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
    saveState(widget, properties[i])
    valueEntry.destroy()
    valueLabel = Label(root.propertiesParent, text=widget[properties[i]])
    valueLabel.grid(row=i, column=1)

def renderProperties(widget,key, self):
    global root; root = self
    global k; k = key
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
        

def saveState(widget, prop):
    global k,root
    activeTabName = root.tabParent.tab(root.tabParent.select(), "text")
    filePath = root.tabEntities['canvas']['entities'][activeTabName]
    root.cacheDict[filePath][str(k)]['self'][prop] = widget[prop]