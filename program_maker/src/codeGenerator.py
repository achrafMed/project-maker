



def GenerateCode(cacheDict):
    for key in cacheDict:
        with open(key, 'w') as f:
            writeWidget(cacheDict[key])



def writeWidget(cacheDictionnary):
    