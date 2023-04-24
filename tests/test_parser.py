
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
import math_json_parser.parser_polars as pp

print("Hello world")
input_file = open (PROJECT_ROOT + '/tests/test_data.json')
json_array = json.load(input_file)


import numexpr as ne
import math
import polars as pl
ImaginaryUnit = complex(0,1)
Pi = math.pi
A = 10
B = 2

pn_test = pn.parser_numexpr()

expr_list = json_array['fn2']
print(expr_list)
expr = pn_test.parser(expr_list)
print(expr)
print(ne.evaluate(expr))



pp_test = pp.parser_polars()
math_json = ["Add", ["Sin",  ["Substract","Pi","B"]], \
        ["Multiply", ["Sqrt","B"], ["Power", "A","B"] ]  ]
# print(math_json[::-1])
func1 = pp_test.parser(math_json)
func2 = pp_test.parser(["Multiply", "A", "Pi"])
func3 = pp_test.parser(json_array["fn2"])

print("The custom function is", func3)
var_dict = {"A": [20, 30], "B":[5, 7]}
cons_dict = {"Pi":3.14}
var_dict.update(cons_dict)
data = pl.DataFrame(var_dict)
objectives = data.select(
    func1.alias("Objective 1"),
    func2.alias("Objective 2"),
)


var_dic2 = {"A":[1,2,3,4,5,6,7,8]}
var_dic2.update(cons_dict)
data2 = pl.DataFrame(var_dic2)
objectives2 = data2.select(
    func3.alias("f3")   
)
print("The output is", objectives2)