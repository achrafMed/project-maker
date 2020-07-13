from tkinter import *
from tkinter.ttk import *
import pathlib
from os import walk

class program(Tk):
    def __init__(self,*args, **kwargs):
        Tk.__init__(self, *args, **kwargs)
        self.geometry("500x500")
        self.tabParent = Notebook(self)
        self.fileFrame = Frame(self)
        self.fileFrame.pack(side=LEFT)
        self.tabs = {}
        self.fileDict = {}
        self.renderDirectoryFiles()

    def renderDirectoryFiles(self):

        self.dirPath = pathlib.Path('C:\\Users\\Dell\\Documents\\programs')
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
                    tempButton = Button(parent, text= file, command=lambda f=file: print(f))
                    output[key].append(tempButton)
                    index+=1
                    tempButton.grid(row=index+1, sticky=W, padx=(10,))
                
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
            output['files'] = files
            break
        return output

test = program()





test.mainloop()