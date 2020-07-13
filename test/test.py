from os import walk
import pathlib

c_path = pathlib.Path(__file__).parent.parent.absolute()

print(c_path)

def breakPaths(path):
    output = {}
    for (p, dirs, files) in walk(path):
        for e in dirs:
            output[e] = breakPaths(str(path) + '/' + e)
        output['files'] = files
        break
    return output

print(breakPaths(c_path))