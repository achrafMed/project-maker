import sys, inspect
import tkinter.ttk
sys.path.insert(0, '../')
def GenerateCode(cacheDict):
    for key in cacheDict:

        writeWidget(cacheDict[key], key)

def removeCode(key: str):
    startIndex: int; endIndex: int
    with open('templates/empty_window.py', 'r') as f:
        fileLines = f.readlines()
        f.close()
    with open(key, 'w') as f:
        f.writelines(fileLines)
        f.close()
def writeWidget(cacheDictionnary: dict, k: str):
    iOut = inspect.getmembers(sys.modules[tkinter.ttk.__name__])
    widgets = [e for e in iOut if inspect.isclass(e[1])]
    fileLines: list
    
    removeCode(k)
    with open(k, 'r') as f:
        fileLines = f.readlines()
        f.close()
    for key in cacheDictionnary.keys():
        if key != 'parent':
            widget = cacheDictionnary[key]['type']
            values = cacheDictionnary[key]['self']
            writable_return = f'        {widget}_{key} = {widget}({keyValueParse(values)})\n        {widget}_{key}.place({keyValueParse(cacheDictionnary[key]["placeProps"], 1)})\n'
            endIndex = fileLines.index('#end widgets\n')
            index = endIndex
            fileLines.insert(index, writable_return)
            fileLines[0] = f'#{str(index+2)}\n'
    with open(k, 'w') as f:
        f.writelines(fileLines)
        f.close()


def keyValueParse(dic, *t) -> str:
    if len(t) == 0:
        string = 'self, '
    else:
        string = ''
    for index, key in enumerate(dic.keys()):
        if index == len(dic.keys())-1:
            if type(dic[key]) == str:
                string += f'{key}="{dic[key]}"'
            else:
                string += f'{key}={dic[key]}'
        else:
            if type(dic[key]) == str:
                string += f'{key}="{dic[key]}", '
            else:
                string += f'{key}={dic[key]}, '
            
    return string

a ={'C:/Users/Dell/Desktop/project_tests/tk_project/main.py': {'parent': {'self': {'type': 'Frame', 'text': 'main.py~design'}}, '0': {'type': 'Button', 'self': {'text': 'text here'}, 'placeProps': {'anchor': 'center', 'x': 25, 'y': 21}}, '1': {'type': 'Checkbutton', 'self': {'text': 'text here'}, 'placeProps': {'anchor': 'center', 'x': 107, 'y': 25}}}}
