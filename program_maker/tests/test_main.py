import sys

sys.path.insert(1, '../')

import unittest

import src.codeGenerator as CG
import json
class testMain(unittest.TestCase):

    def test_CodeGenerator(self):
        with open('C:/Users/Dell/Desktop/project_tests/tk_project/.cache', 'r') as f:
            cacheDict = json.load(f)
            CG.GenerateCode(cacheDict)
            CG.GenerateCode(cacheDict)