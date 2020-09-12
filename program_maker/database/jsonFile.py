
class splitter:
    def __init__(self):
        self.string = ''
        self.array = list()# self.array = []
        self.curly = list()
        self.quotes = list()
        self.c_curly = list()
        self.main_c = list()#the ùain curly brackets
        self.t_strings = list()


    def __cut(self, string):
        islist = False
        if len(string) == 0:
            return []
        if string[0] == '{'or string[0] == '[':
            if string[0] == '[':
                islist = True
            value = string[1:len(string)-1]
        else:
            value = string
        quotes = self.get_strings(value)
        #getting the curly brackets
        index = 0
        char = '{'
        curlies = [[],[]]

        while True:
            if value.find(char, index) == -1:
                if char == '{':
                    char = '}'
                    index = 0
                    pass
                else:
                    index = 0
                    break
            else:
                index = value.find(char,index) + 1
                if char == '{':
                    curlies[0].append(index -1)
                else:
                    curlies[1].append(index - 1)
        #sorting the curlies
        if len(curlies[0]) != len(curlies[1]):
            #print(value)
            print("ERROR: cut")
            return
        index = 0
        while True:
            if len(curlies[0]) == 0:
                break
            if len(curlies[0]) == 1:
                self.curly.append((curlies[0][0],curlies[1][0]))
                self.main_c.append((curlies[0][0],curlies[1][0]))
                break
            if index >= len(curlies[0]) - 1:
                if index -1 == 0:
                    self.main_c.append((curlies[0][0],curlies[1][0]))
                self.curly.append((curlies[0][index-1],curlies[1][0]))
                curlies[0].pop(index-1)
                curlies[1].pop(0)
                index -= 2
            elif curlies[0][index] > curlies[1][0]:
                if index -1 == 0:
                    self.main_c.append((curlies[0][0],curlies[1][0]))
                self.curly.append((curlies[0][index-1],curlies[1][0]))
                curlies[0].pop(index-1)
                curlies[1].pop(0)
                index -= 1
            else:
                index += 1

        index = 0
        coms = self.get_com(value, quotes)
        if islist == True:
            for com in coms:
                for c in self.main_c:
                    if com > c[0] and com < c[1]:
                        coms.remove(com)
        lis = self.get_list(value, quotes)
        lis = lis[0] + lis[1] + self.main_c
        res = list()
        while True:
            if len(coms) == 0:
                res.append(value[index:])
                break
            elif not self.is_inside(coms[0], lis):
                res.append(value[index:coms[0]])
                index = coms[0] + 1
                coms.pop(0)
            else:
                coms.pop(0)
        #print(res)
        return res

    def cut(self, string):
        self.__init__()
        out = self.__cut(string)
        return out

    def get_list(self, string, quotes):
        res = [[],[]] #first array is lists, second is tuples
        char = '['
        index = 0
        array1 = [[],[]]
        array2 = [[],[]]
        while True:
            if string.find(char, index) == -1:
                if char == '[':
                    char = ']'
                    index = 0
                    pass
                elif char == ']':
                    char = '('
                    index = 0
                    pass
                elif char == '(':
                    index = 0
                    char = ')'
                    pass
                else:
                    break
            elif self.is_inside(string.find(char, index), quotes):
                pass
            else:
                # index != -1
                index = string.find(char, index)
                if char == '[':
                    array1[0].append(index)
                elif char == ']':
                    array1[1].append(index)
                elif char == '(':
                    array2[0].append(index)
                else:
                    array2[1].append(index)
                index += 1
        if len(array1[0]) != len(array1[1]) or len(array2[0]) != len(array2[1]):
            print("ERROR: get_list")
            return
        index = 0

        n = 0 #indentifies which array to choose
        while True:
            if len(array1[0]) == 0:
                if len(array2[0]) == 0:
                    break
                    pass
                else:
                    n = 1
                array1 = array2
                index = 0
                pass
            if len(array1[0]) == 1:
                res[n].append((array1[0][0], array1[1][0]))
                if n == 1:
                    break
                    pass
                else:
                    array1[0].pop(0)
                    array1[1].pop(0)
                    pass
            else:
                if array1[0][index] > array1[1][0]:
                    res[n].append((array1[0][index-1], array1[1][0]))
                    array1[1].pop(index-1)
                    index -= 1
                    array1[0].pop(0)
                else:
                    index += 1
        return res


    def get_com(self,string, quotes):
        index = 0
        res = list()
        value = str()
        if len(string) == 0:
            return []
        else:
            value = string
            quotes = self.get_strings(value)
            lis = self.get_list(value, quotes)
        while True:
            if value.find(',', index) == -1:
                break
            else:
                index = value.find(',', index)
                if not self.is_inside(index, lis[0]) and not self.is_inside(index, lis[1]):
                    res.append(index)
                index += 1
        return res


    def get_strings(self, string):
        array = list()
        index = 0
        char = "'"
        while True:
            index = string.find(char, index)
            if index == -1:
                if char == "'":
                    char = '"'
                    index = 0

                elif char == '"':
                    break
            elif string.find(char, index+1 ) == -1:
                print('ERROR: missing apostrofie at {}'.format(index))
                #print(string)
                break
            else:
                array.append((index, string.find(char, index+1)))
                index = string.find(char, index+1) + 1
        #print(array)
        return array
    def is_inside(self, inIndex, array):
        for element in array:
            if inIndex < element[1] and inIndex > element[0]:
                return True
        return False
    def type(self, string):
        l_str = list(string)
        while True:
            if len(l_str) == 0:
                break
            if l_str[0] == ' ':
                l_str.pop(0)
            else:
                break
        string = ''.join(l_str)
        if string[0] == '[':
            return 'list'
        elif string[0] == '(':
            return 'tuple'
        elif string[0] == '{':
            return 'dictionnary'

        try:
            res = int(string)
            return 'int'
        except ValueError:
            if string.find('{') == -1 and string.find('[') == -1 and string.find('(') == -1:
                return 'string'
            else:
                strings = self.get_strings(string)

                self.t_strings = strings
                res = ''
                char = '{'
                index = 0
                while True:
                    if string.find(char, index) == -1:
                        if char == '{':
                            char = '['
                            index = 0
                            pass
                        elif char == '[':
                            char = '('
                            index = 0
                            pass
                        else:
                            res = 'string'
                            break
                    else:
                        if len(strings) == 0:
                            if char == '{':
                                return 'dictionnary'
                            elif char == '(':
                                return 'tuple'
                            else:
                                return 'list'
                        for e in strings:
                            if string.find(char, index) < e[1] and string.find(char, index) > e[0]:
                                pass
                            else:
                                if char == '{':
                                    res = 'dictionnary'
                                elif char == '(':
                                    res = 'tuple'
                                else:
                                    res = 'list'
                                break
                        if res != '':
                            break
                        else:
                            index = string.find(char, index) + 1
                return res








spl = splitter()
class json:
    def __init__(self, type='null'):
        self.type = type
        self.string = ''
        self.split = splitter()
        self.dic = {}
        self.out = list()
        self.remain = "vide"
        self.index = 0
        self.t = 'dic'
        self.main = True
    def dict_to_string(self, dicname, dic):
        self.string = '{' + '"' + dicname +  '"'+ ":" + str(dic) + '}'
        return self.string


    def tf(self, string):


        t = self.split.type(string)
        if t == 'int':
            return int(string)

        elif t == 'string':
            quotes = self.split.get_strings(string)
            main = (len(string), len(string))
            for q in quotes:
                if q[0] < main[0]:
                    main = q
            return string[main[0] + 1: main[1]]
        elif t == 'list':
            output = list()
            value = string[string.find('['):]
            l_str = self.split.cut(value)
            for st in l_str:
                output.append(self.tf(st))
            return output
        elif t == 'dictionnary':
            output = {}
            output = self.str_to_dict(string)
            return output
        else:
            return None


    def str_to_dict(self, string):

        l_str = list(string)
        while True:
            if l_str[0] == ' ':
                l_str.pop(0)
            else:
                break
        string = ''.join(l_str)

        if len(string) == 0:
            return {}
        if string[0] == '{':
            value = string[1:len(string)-1]
        else:
            value = string
        split = splitter()
        l_str = split.cut(value)
        index = 0
        output = {}
        for st in l_str:
            i = st.find(':')
            name = st[:i]
            content = st[i+1:]
            strs = self.split.get_strings(name)
            main = tuple()
            main = (len(name),len(name))

            for e in strs:
                if e[0] < main[0]:
                    main = e
            name = name[main[0]+1:main[1]]
            output[name] = self.tf(content)
        return output

    def reset(self):
        self.__init__()
    def string_to_dict(self, string):
        out = self.str_to_dict(string)
        self.reset()
        return out
dict = {
    'clients': [
        {'name': 'achraf', 'card': 25478},
        {'name': 'ahmed', 'card': 8974}
    ],
    'solde': [50000, 580]
}
test = "{'name': 'achraf', 'fam'; {'parents': '', 'siblings':''}}"

dic = json()

print(dic.string_to_dict(test))
