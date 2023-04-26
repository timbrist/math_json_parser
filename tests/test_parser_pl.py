import json
# from math_json_parser.parser_numexpr import parser_numexpr
import os
import sys
PROJECT_ROOT = os.path.abspath(os.path.join(
                  os.path.dirname(__file__), 
                  os.pardir)
)
sys.path.append(PROJECT_ROOT)
print(PROJECT_ROOT)
import math_json_parser.parser_polars as pp
import random 
import polars as pl
import math
#pytest -q test_parser_ne.py
class TestClass:
    pp_test = pp.parser_polars()
    def test_function(self):
        test_case = [ ["Sqrt","x"],
                    ["Exp","x"],
                    ["Abs","x"],
                    ["Sin","x"],#5
                    ["Cos","x"],
                    ["Tan","x"],
                    ["Arcsin","A"],
                    ["Arccos","x"],
                    ["Arctan","x"],#10 
                    ["Sinh","x"],
                    ["Cosh","x"],
                    ["Tanh","x"],
                    ["Arcsinh","x"],
                    ["Arccosh","b"],#15
                    ["Arctanh","x"],
                    ["Ln","x"],
                    ["Lg","x"],
                    ["LogOnePlus","x"],
        ]
        step = 0
        for expr in test_case:
            print(expr)
            # print(step)
            a = self.pp_test.parser(expr) 
            print(a)
        

test = TestClass()
test.test_function()