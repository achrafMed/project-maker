from tkinter import *
from tkinter.ttk import *


def createMenu(root, parent):
    root.config(menu=parent)
    fileMenu = Menu(parent)
    fileMenu.add_command(label="open folder", command=root.renderDirectoryFiles)
    fileMenu.add_command(label="save", command=lambda e=root: saveChange(e))
    fileMenu.add_command(label="create tkinter project", command=lambda:  root.createTkinterProject(root.dirPath))
    fileMenu.add_command(label="Exit", command=root._quit)
    parent.add_cascade(label="File", menu=fileMenu)

    editMenu = Menu(root.menu)
    editMenu.add_command(label="Undo")
    editMenu.add_command(label="Redo")
    parent.add_cascade(label="Edit", menu=editMenu)

    windowMenu = Menu(root.menu)
    windowMenu.add_command(label="refresh", command= lambda e=root: refreshApp(e))
    parent.add_cascade(label="window", menu=windowMenu)
def saveChange(root):
    for key in root.tabEntities.keys():
        if key != 'canvas':
            root.saveFile(key)


def refreshApp(root):
    root.renderDirectoryFiles(root.dirPath)