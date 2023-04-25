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
    def test_one_parameter(self):
        test_case = ["Sqrt","x"]
        x = random.uniform(1, 10)
        assert ne.evaluate( self.pn_test.parser(test_case)) == math.sqrt(x)

