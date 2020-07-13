from tkinter import * 
from tkinter.ttk import *
from os import walk
import pathlib
root = Tk()
open = False

root.geometry("1000x1000")
a = 250
b=250
button = Label(root, text="hi")
label = Label(root, text='hello')
label.place(x=100, y=100)
def hello(event):
    d = root.winfo_pointerx()-root.winfo_rootx()
    c = root.winfo_pointery()-root.winfo_rooty()
    print('{}, {}'.format(d,c))
    button.place_forget()
    
    button.place(x=d, y=c, anchor='center')
r_path = pathlib.Path(__file__).parent.absolute()


button.bind('<B1-Motion>', hello)
button.place(x=a,y=b,anchor="center")
def activate(frame, i):

    if frame.winfo_ismapped() == 0:
        frame.grid(row=i+1)
    else:
        frame.grid_forget()



def renderBlock(parent, fileDict):
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
                tempButton.grid(row=index+1, sticky=W)
                
        else:
            temp =  {}
            temp['frameParent'] = Frame(parent)
            temp['self'] = Button(parent, text=key, command=lambda frame=temp['frameParent'], i=index: activate(frame, i))
            temp['self'].grid(row=index, sticky=W)
            print("{} {}".format(key, index))
            index+=2
            temp.update(renderBlock(temp['frameParent'], fileDict[key]))
            output = temp

    return output
def breakPaths(path):
    output = {}
    for (p, dirs, files) in walk(path):
        for e in dirs:
            output[e] = breakPaths(str(path) + '/' + e)
        output['files'] = files
        break
    return output
frameParent = Frame(root)
frame1 = Frame(frameParent)

label = Label()

fileFrame = Frame(root)
fileFrame.pack()
dirPath = pathlib.Path(__file__).parent.absolute()

test = breakPaths(dirPath)
print(test)
renderBlock(fileFrame, test)


drop = Button(frame1, text='drop', command=activate)
drop.pack(ipadx=30)

frame2 = Frame(frameParent)

fileButton = Button(frame2, text='option1')
fileButton.pack(padx=(10,0))

fileButton.forget()

frameParent.pack()
frame1.pack()
frame2.pack()

notebook = Notebook(root)
notebook.pack()
f = Frame(notebook)
f_label = Label(f, text="jellooo")
f_label.pack()

notebook.add(f, text="1")


root.mainloop()
print('rem')