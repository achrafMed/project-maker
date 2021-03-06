from tkinter import *
import json
from tkinter.ttk import *
import tkinter.filedialog as filedialog
import pathlib
import sys, inspect
from os import walk, mkdir
from os import path as osPath
from src.properties import renderProperties
from src.protocols import close
from src.codeGenerator import GenerateCode
from src.menuHandler import *
from src.keyBindings import *

class program(Tk):
    def __init__(self,*args, **kwargs):
        Tk.__init__(self, *args, **kwargs)
        import tkinter.ttk
        iOut = inspect.getmembers(sys.modules[tkinter.ttk.__name__])
        self.widgets = [e for e in iOut if inspect.isclass(e[1])]
        self.tkFile = ""
        self.geometry("500x500")
        self.tabParent = Notebook(self)
        self.fileFrame = Frame(self)
        self.fileFrame.pack(side=LEFT, anchor=NE)
        self.tabParent.pack(side=LEFT, fill=BOTH, expand=1)
        self.tabs = {}
        self.fileDict = {}
        self.cacheDict = {}
        self.tabEntities = {}
        self.tabEntities['canvas'] = {}
        self.tabEntities['canvas']['entities'] = {}
        self.widgetContainer = Frame(self)
        self.widgetContainer.pack(side=RIGHT)
        self.widgetParent = Frame(self.widgetContainer)
        self.widgetParent.pack(side=TOP)
        self.propertiesParent = Frame(self.widgetContainer)
        self.propertiesParent.pack(side=BOTTOM)
        self.renderDirectoryFiles()
        self.canvasEntities = list()
        self.menu = Menu(self)
        self.bind()
        createMenu(self, self.menu)
        close(self, self._quit)
    def _quit(self):
        try:
            with open(self.dirPath + '/tk_project/.cache/components.json', 'w') as f:

                json.dump(self.cacheDict, f)
                f.close()
        except:
            try:
                with open(self.dirPath + '/.cache/components.json') as f:
                    json.dump(self.cacheDict, f)
                    f.close()
            except:
                self.quit()
                return
        GenerateCode(self.cacheDict)
        self.quit()
    def renderDirectoryFiles(self, dirPath=''):
        self.tabParent.destroy()
        self.fileFrame.destroy()

        self.tabParent = Notebook(self)
        self.fileFrame = Frame(self)
        self.fileFrame.pack(side=LEFT, anchor=NE)
        self.tabParent.pack(side=LEFT, fill=BOTH, expand=1)
        if len(dirPath) != 0:
            self.dirPath = dirPath
        else:
            self.dirPath = self.openFileDialog()
        folderTabData = self.breakPaths(self.dirPath)
        self.fileDict = folderTabData
        self.fileFrameEntities = self.renderBlock(self.fileFrame, self.fileDict)
        self.fileDict = {}
        self.cacheDict = {}
        self.tabEntities = {}
        self.tabEntities['canvas'] = {}
        self.tabEntities['canvas']['entities'] = {}
        try:
            self.openTkCanvas()
        except:
            pass
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

        with open(filePath + "/tk_project/.cache/components.json", "w+") as f:
            f.close()
        self.renderDirectoryFiles()
        self.tkFile = filePath + "/tk_project/main.py"
        self.tkFileCache = filePath + "/tk_project/.cache/components.json"
        self.createTkCanvas(self.tkFile)

    def openFileDialog(self):
        folderPath = filedialog.askdirectory(title="open folder")
        return folderPath
    def openTkCanvas(self):
        try:
            tkFileCache = self.dirPath+ "/.cache/components.json"
            with open(tkFileCache, 'r') as f:
                try:
                    cacheDict = json.load(f)
                except json.decoder.JSONDecodeError:
                    cachDict = {}
                self.cacheDict = cacheDict
                for key in list(cacheDict.keys()):
                    if key != '':
                        self.createTkCanvas(key)
                f.close()
        except:
            tkFileCache = self.dirPath+ "/tk_project/.cache/components.json"
            with open(tkFileCache, 'r') as f:
                try:
                    cacheDict = json.load(f)
                except json.decoder.JSONDecodeError:
                    cachDict = {}
                self.cacheDict = cacheDict
                for key in list(cacheDict.keys()):
                    if key != '':
                        self.createTkCanvas(key)
                f.close()

    def createTkCanvas(self, filePath):
        tkCanvas = Frame(self.tabParent)
        CanvasName = filePath.split('/')[len(filePath.split('/'))-1]
        if CanvasName in list(self.tabEntities['canvas']['entities'].keys()):
            CanvasName = "{}/{}~design".format(filePath.split('/')[len(filePath.split())-2],filePath.split('/')[len(filePath.split())-1])
        else:
            CanvasName +='~design'
        self.tabParent.add(tkCanvas, text=CanvasName)
        self.tabEntities['canvas'][filePath] = {}
        self.tabEntities['canvas'][filePath]['self'] = tkCanvas
        self.tabEntities['canvas'][filePath]['children'] = []
        self.tabEntities['canvas']['entities'][CanvasName] = filePath
        try:
            fileComponents = self.cacheDict[filePath]
            self.renderTkWidgets(fileComponents)
            self.renderWidgetGallery()
            self.cacheDict[filePath]['parent']['self'] = {'type': 'Frame', "text": CanvasName}
        except KeyError:
            self.cacheDict[filePath] = {}
            self.renderWidgetGallery()
            self.cacheDict[filePath]['parent'] = {}
            self.cacheDict[filePath]['parent']['self'] = {'type': 'Frame', 'text': CanvasName}
    def renderTkWidgets(self, fileComponents):
        filePath = [e for e in list(self.cacheDict.keys()) if self.cacheDict[e] == fileComponents][0]
        
        canvas = self.tabEntities['canvas'][filePath]['self']
        for key in list(fileComponents.keys()):
            if key != "parent":
                widget = [e[1] for e in self.widgets if fileComponents[key]['type'] == e[0]][0]
                w = widget(canvas, text= fileComponents[key]['self']['text'])
                w.bind('<B1-Motion>', lambda e, index=key: self.moveWidgetWithCursor(e, index))
                w.place(x= fileComponents[key]['placeProps']['x'], y=fileComponents[key]['placeProps']['y'])
                w.bind('<Button-1>', lambda e, widget=w,k=key ,parent=self: renderProperties(widget,k, parent))
                self.tabEntities['canvas'][filePath]['children'].append((int(key), w))

    def renderWidgetGallery(self):
        objWidgets = list(map(lambda e: Button(self.widgetParent, text=e[0], command= lambda a=e[0]: self.addWidgetToCanvas(a)), self.widgets))
        for widget in objWidgets:
            widget.pack(side=TOP)
    def moveWidgetWithCursor(self, event, index):
        
        activeTabName = self.tabParent.tab(self.tabParent.select(), "text")
        filePath = self.tabEntities['canvas']['entities'][activeTabName]
        widget = event.widget       
        parent = Widget._nametowidget(self, widget.winfo_parent())
        parent = Widget._nametowidget(self, parent.winfo_parent())
        xpos, ypos = self.winfo_pointerx()- self.winfo_x()-8-parent.winfo_x(), self.winfo_pointery()- self.winfo_y()-50-parent.winfo_y()-23
        widget.place_forget()
        widget.place(x=xpos, y=ypos)
        self.cacheDict[filePath][str(index)]['placeProps'].pop('relx', None)
        self.cacheDict[filePath][str(index)]['placeProps'].pop('rely', None)
        self.cacheDict[filePath][str(index)]['placeProps']['x'], self.cacheDict[filePath][str(index)]['placeProps']['y'] = xpos, ypos

    def addWidgetToCanvas(self, widgetName):
        activeTabName = self.tabParent.tab(self.tabParent.select(), "text")
        try:
            filePath = self.tabEntities['canvas']['entities'][activeTabName]
        except KeyError:
            return
        indexes = [b[0] for b in self.tabEntities['canvas'][filePath]['children']]
        try:
            index = max(indexes) + 1
        except ValueError:
            index = 0
        widget = [e[1] for e in self.widgets if e[0] == widgetName][0]
        w = widget(self.tabEntities['canvas'][filePath]['self'], text="text here")
        w.bind('<B1-Motion>', lambda event, e=index: self.moveWidgetWithCursor(event, e))
        w.bind('<Button-1>', lambda e, widget=w, parent=self: renderProperties(widget, parent))
        w.place(relx=0.5, rely=0.5, anchor='center')
        widgetDict = {
            'type': widgetName,
            'self': {
                'text': "text here"
            },
            'placeProps': {'relx': 0.5, 'rely': 0.5, 'anchor': NW}
        }
        self.tabEntities['canvas'][filePath]['children'].append((index, widgetDict))
        self.cacheDict[filePath][str(index)] = widgetDict

test = program()



test.mainloop()
