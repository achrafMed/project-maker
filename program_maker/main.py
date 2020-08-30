from tkinter import *

from tkinter.ttk import *
import tkinter.filedialog as filedialog
import pathlib
import sys, inspect
from os import walk, mkdir
from os import path as osPath
from database.jsonFile import json, splitter
class program(Tk):
    def __init__(self,*args, **kwargs):
        Tk.__init__(self, *args, **kwargs)
        self.js = json()
        self.tkFile = ""
        self.geometry("500x500")
        self.tabParent = Notebook(self)
        self.fileFrame = Frame(self)
        self.fileFrame.pack(side=LEFT, anchor=NE)
        self.tabParent.pack(side=LEFT, fill=BOTH, expand=1)
        self.tabs = {}
        self.fileDict = {}

        self.tabEntities = {}
        self.tabEntities['canvas'] = {}
        self.tabEntities['canvas']['entities'] = {}
        self.widgetParent = Frame(self)
        self.widgetParent.pack(side=RIGHT)
        self.renderDirectoryFiles()
        self.canvasEntities = list()
        self._createMenu()
    def _createMenu(self):
        self.menu = Menu(self)
        self.config(menu=self.menu)

        fileMenu = Menu(self.menu)
        fileMenu.add_command(label="open folder", command=self.renderDirectoryFiles)
        fileMenu.add_command(label="create tkinter project", command=lambda:  self.createTkinterProject(self.dirPath))
        fileMenu.add_command(label="Exit", command=self.quit)
        self.menu.add_cascade(label="File", menu=fileMenu)

        editMenu = Menu(self.menu)
        editMenu.add_command(label="Undo")
        editMenu.add_command(label="Redo")
        self.menu.add_cascade(label="Edit", menu=editMenu)
    def renderDirectoryFiles(self):
        self.tabParent.destroy()
        self.fileFrame.destroy()
        
        self.tabParent = Notebook(self)
        self.fileFrame = Frame(self)
        self.fileFrame.pack(side=LEFT, anchor=NE)
        self.tabParent.pack(side=LEFT, fill=BOTH, expand=1)
        self.dirPath = self.openFileDialog()
        folderTabData = self.breakPaths(self.dirPath)
        self.fileDict = folderTabData
        self.fileFrameEntities = self.renderBlock(self.fileFrame, self.fileDict)
    def renderBlock(self, parent, fileDict):
        index = 0
        output = {}
        keys = list(fileDict.keys())
        for key in keys:
            if key == 'files':
                output[key] = list()
                for file in fileDict['files']:
                    tempButton = Button(parent, text= file, command=lambda path=fileDict['dir'], f=file: self.addTab(path, f))
                    output[key].append(tempButton)
                    index+=1
                    tempButton.grid(row=index+1, sticky=W, padx=(10,))
            elif key == 'dir':
                pass  
            else:
                temp =  {}
                temp['frameParent'] = Frame(parent)
                temp['self'] = Button(parent, text=key, command=lambda frame=temp['frameParent'], i=index: self.activate(frame, i))
                if parent != self.fileFrame:
                    temp['self'].grid(row=index, sticky=W, padx=(10,))
                else:
                    temp['self'].grid(row=index, sticky=W)

                index+=2
                temp.update(self.renderBlock(temp['frameParent'], fileDict[key]))
                
                output = temp

        return output
    def activate(self, frame, index):
        if frame.winfo_ismapped() == 0:
            frame.grid(row=index+1)
        else:
            frame.grid_forget()

    
    def breakPaths(self, path):
        output = {}
        for (p, dirs, files) in walk(path):
            for e in dirs:
                output[e] = self.breakPaths(str(path) + '/' + e)
            output['dir'] = p
            output['files'] = files
            break
        return output
    def addTab(self,path, name):
        filePath = osPath.join(path, name)
        self.tabEntities[filePath] = {}
        tabFrame = Frame(self.tabParent)
        self.tabEntities[filePath]['self'] = tabFrame
        self.tabParent.add(tabFrame, text=name)
        self.tabEntities[filePath]['text'] = Text(tabFrame, tabs=('8m',))
        self.tabEntities[filePath]['text'].pack(fill=BOTH, expand=1)
        self.tabEntities[filePath]['save'] = Button(tabFrame, text="save", command=lambda p=filePath: self.saveFile(p))
        self.tabEntities[filePath]['save'].pack()
        with open(filePath, "r") as func:
            try:
                text = func.readlines()
                for line in text:
                    self.tabEntities[filePath]['text'].insert(END, line)
            except UnicodeDecodeError:
                self.tabEntities[name]['text'].insert(END, "can't open this file")
    def saveFile(self, filePath):
        #wText is the text widget
        text = self.tabEntities[filePath]['text'].get('1.0', END)
        with open(filePath, "w+") as f:
            f.write(text)
            f.close()
    def createTkinterProject(self, filePath):
        templateText = list()
        with open("templates/empty_window.py", "r") as f:
            templateText = f.readlines()
            f.close()
        mkdir(filePath + '/tk_project')
        mkdir(filePath + '/tk_project/.cache')
        with open(filePath + "/tk_project" + "/main.py", "w+") as f:
            f.writelines(templateText)
            f.close()

        with open(filePath + "/tk_project/.cache/components.txt", "w+") as f:
            f.write('cahe file')
            f.close()
        self.renderDirectoryFiles()
        self.tkFile = filePath + "/tk_project/main.py"
        self.tkFileCache = filePath + "/tk_project/.cache/components.txt"
        self.createTkCanvas(self.tkFile)

    def openFileDialog(self):
        folderPath = filedialog.askdirectory(title="open folder")
        return folderPath

    def createTkCanvas(self, filePath):
        tkCanvas = Canvas(self.tabParent)
        CanvasName = filePath.split('/')[len(filePath.split('/'))-1]
        if CanvasName in list(self.tabEntities['canvas']['entities'].keys()):
            CanvasName = "{}/{}~design".format(filePath.split('/')[len(filePath.split())-2],filePath.split('/')[len(filePath.split())-1])
        else:
            CanvasName +='~design'
        with open(self.tkFileCache, 'r') as f:
            tkFileDict = f.readlines()
            fileDict = self.js.string_to_dict(tkFileDict)
            f.close()
        self.tabParent.add(tkCanvas, text=CanvasName)

        self.tabEntities['canvas'][filePath] = {}
        self.tabEntities['canvas'][filePath]['self'] = tkCanvas
        self.tabEntities['canvas'][filePath]['children'] = []
        self.tabEntities['canvas']['entities'][CanvasName] = filePath
        try:
            fileComponents = fileDict[filePath]
            self.renderWidgetGallery()
        except KeyError:
            fileDict[filePath] = {}
            self.renderWidgetGallery()
    def renderWidgetGallery(self):

        import tkinter.ttk
        iOut = inspect.getmembers(sys.modules[tkinter.ttk.__name__])
        widgets = [e for e in iOut if inspect.isclass(e[1])]
        objWidgets = list(map(lambda e: Button(self.widgetParent, text=e[0], command= lambda a=e[1]: self.addWidgetToCanvas(a)), widgets))
        for widget in objWidgets:
            widget.pack(side=TOP)
    def moveWidgetWithCursor(self, event, widget):
        parent = Widget._nametowidget(self, widget.winfo_parent())
        width, height = parent.winfo_width()/2, parent.winfo_height()/2
        locx, locy = widget.winfo_x(), widget.winfo_y()
        w , h =self.winfo_width(),self.winfo_height()
        mx ,my =widget.winfo_width(),widget.winfo_height()
        xpos=(locx+event.x)-(15)
        ypos=(locy+event.y)-int(my/2)
        if xpos>=0 and ypos>=0 and w-abs(xpos)>=0 and h-abs(ypos)>=0 and xpos<=w-5 and ypos<=h-5:
            widget.place(x=xpos-width,y=ypos-height)



        #
        
    def addWidgetToCanvas(self, widget):
        activeTabName = self.tabParent.tab(self.tabParent.select(), "text")
        try:
            filePath = self.tabEntities['canvas']['entities'][activeTabName]
        except KeyError:
            pass
        indexes = [b[0] for b in self.tabEntities['canvas'][filePath]['children']]
        try:
            index = max(indexes) + 1
        except ValueError:
            index = 0
        w = widget(self.tabEntities['canvas'][filePath]['self'], text="text here")
        w.bind('<B1-Motion>', lambda event, e=w: self.moveWidgetWithCursor(event, e))
        w.place(relx=0.5, rely=0.5, anchor='center')
        self.tabEntities['canvas'][filePath]['children'].append((index, w))
test = program()




test.mainloop()
