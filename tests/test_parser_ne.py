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
import math_json_parser.parser_numexpr as pn
import random 
import numexpr as ne
import math
#pytest -q test_parser_ne.py
class TestClass:
    pn_test = pn.parser_numexpr()
    def test_function(self):
        test_case = [ ["Sqrt","x"],
                    ["Exp","x"],
                    ["Expm1","x"],
                    ["Abs","x"],
                    ["Sin","x"],#5
                    ["Cos","x"],
                    ["Tan","x"],
                    ["Arcsin","A"],
                    ["Arccos","x"],
                    ["Arctan","x"],#10 
                    #["Arctan2","x","x"],
                    ["Sinh","x"],
                    ["Cosh","x"],
                    ["Tanh","x"],
                    ["Arcsinh","x"],
                    ["Arcosh","b"],#15
                    ["Arctanh","x"],
                    ["Ln","x"],
                    ["Lg","x"],
                    ["LogOnePlus","x"],
        ]
        x = random.uniform(0, 1)
        A = random.uniform(-1, 1)
        b = random.uniform(1,10)
        test_result = [
            math.sqrt(x),
            math.exp(x),
            math.expm1(x),
            abs(x),
            math.sin(x),
            math.cos(x),
            math.tan(x),
            math.asin(A),
            math.acos(x),
            math.atan(x),
            #math.atan2(x,x),
            math.sinh(x),
            math.cosh(x),
            math.tanh(x),
            math.asinh(x),
            math.acosh(b),
            math.atanh(x),
            math.log(x),
            math.log10(x),
            math.log1p(x)
        ]
        step = 0
        for expr in test_case:
            # print(expr)
            # print(step)
            # a = self.pn_test.parser(expr) 
            # print(ne.evaluate(a))
            assert ne.evaluate( self.pn_test.parser(expr)) == test_result[step]
            step +=1
        

# test = TestClass()
# test.test_function()