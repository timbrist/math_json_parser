import math
import json
import os
import sys
PROJECT_ROOT = os.path.abspath(os.path.join(
                  os.path.dirname(__file__), 
                  os.pardir)
)
sys.path.append(PROJECT_ROOT)
print(PROJECT_ROOT)
import math_json_parser.parser_polars as pp
import polars as pl
import pytest
import numpy as np

OPERATROS_CASES = [
        ["Max","A"],
        ["Min","A"],
        ["Sum","A"],
        ["Product","A"], 
]
RELATIONAL_CASES = [
        ["Equal","A","B"],
        ["Greater","A","B"],
        ["GreaterEqual","A","B"],
        ["Less","A","B"],
        ["LessEqual","A","B"],#5
        ["NotEqual","A","B"],
]
FUNCTION_CASES = [
        ["Add","A","B"],
        ["Substract","A","B"],
        ["Negate","A"],
        ["Multiply","A","B"],#10
        ["Divide","A","B"],
        ["Power","A","B"],
        ["Sqrt","A"],
]
TRANSCENDENTAL_CASES = [
        ["Exp","A"],
        ["Ln","A"],#30
        ["Log","A",4],
        ["Lb","A"],
        ["Lg","A"],
        ["LogOnePlus","A"],
]
ROUNDING_CASES = [
        ["Abs","A"],
        ["Ceil","X"],
        ["Floor","X"],#35
]
TRIGONOMETRIC_CASES = [
        ["Arccos","A"],
        ["Arccosh","A"],
        ["Arcsin","A"],
        ["Arcsinh","A"],
        ["Arctan","A"],#20
        ["Arctanh","A"],
        ["Cos","A"],
        ["Cosh","A"],
        ["Sin","A"],#25
        ["Sinh","A"],
        ["Tan","A"],
        ["Tanh","A"],
]



def test_simple_expr():
    #one operator test case
    expected_operators = [
        str(pl.col("A").max()),
        str(pl.col("A").min()),
        str(pl.col("A").sum()),
        str(pl.col("A").product()), 
    ]
    expected_relational = [
        str(pl.col("A") == pl.col("B")),
        str(pl.col("A") > pl.col("B")),
        str(pl.col("A") >= pl.col("B")),
        str(pl.col("A") < pl.col("B")),
        str(pl.col("A") <= pl.col("B")),
        str(pl.col("A") != pl.col("B")),
    ]
    expected_funtions = [
        str(pl.col("A") + pl.col("B")),
        str(pl.col("A") - pl.col("B")),
        str(-pl.col("A")),
        str(pl.col("A") * pl.col("B")),
        str(pl.col("A") / pl.col("B")),
        str(pl.col("A") ** pl.col("B")),
        str(pl.col("A") ** (1/2)),
    ]
    expected_transcendental = [
        str(pl.col("A").exp()),
        str(pl.col("A").log()),
        str(pl.col("A").log(base=4)),
        str(pl.col("A").log(base=2)),
        str(pl.col("A").log10()),
        str(pl.col("A").log1p()),
    ]
    expected_rouding = [
        str(pl.col("A").abs()),
        str(pl.col("X").ceil()),
        str(pl.col("X").floor()),
    ]
    excepted_trigonometric =[
        str(pl.col("A").arccos()),
        str(pl.col("A").arccosh()),
        str(pl.col("A").arcsin()),
        str(pl.col("A").arcsinh()),
        str(pl.col("A").arctan()),
        str(pl.col("A").arctanh()),
        str(pl.col("A").cos()),
        str(pl.col("A").cosh()),
        str(pl.col("A").sin()),
        str(pl.col("A").sinh()),
        str(pl.col("A").tan()),
        str(pl.col("A").tanh()),
    ]
    test_pp = pp.parser_polars()
    for i in range(len(OPERATROS_CASES)):
        test_result = test_pp.parser(OPERATROS_CASES[i])
        assert str(test_result) == expected_operators[i]
    for i in range(len(RELATIONAL_CASES)):
        test_result = test_pp.parser(RELATIONAL_CASES[i])
        assert str(test_result) == expected_relational[i]
    for i in range(len(FUNCTION_CASES)):
        test_result = test_pp.parser(FUNCTION_CASES[i])
        assert str(test_result) == expected_funtions[i]
    for i in range(len(TRANSCENDENTAL_CASES)):
        test_result = test_pp.parser(TRANSCENDENTAL_CASES[i])
        assert str(test_result) == expected_transcendental[i]
    for i in range(len(ROUNDING_CASES)):
        test_result = test_pp.parser(ROUNDING_CASES[i])
        assert str(test_result) == expected_rouding[i]
    for i in range(len(TRIGONOMETRIC_CASES)):
        test_result = test_pp.parser(TRIGONOMETRIC_CASES[i])
        assert str(test_result) == excepted_trigonometric[i]

# #This function test parser to handle constant number 
# def test_simple_constant():
#     #integer test cases
#     a = np.random.randint(1,10,size=(5))
#     b = np.random.randint(1,10,size=(5))
#     #  
#     x1 = np.random.uniform(-1,1,size=(5))
#     x2 = np.random.uniform(1,100,size=(5)) 
#     print(x1)
#     expected = [
#         a == b,
#         a >  b,
#         a >= b,
#         a <  b,
#         a <= b,
#         a != b,
#         a +  b,
#         a -  b,
#         -a,
#         a *  b,
#         a /  b,
#         a ** b,
#         a ** (1/2),
#         np.absolute(a),
#         np.unique(a),
#         np.arccos(x1),
#         np.arccosh(a),
#         np.arcsin(x1),
#         np.arcsinh(a),
#         np.arctan(a),
#         np.arctanh(x1),
#         np.unique(a),
#         np.cos(a),
#         np.cosh(a),
#         np.sin(a),
#         np.sinh(a),
#         np.tan(a),
#         np.tanh(a),
#         np.exp(a),
#         np.log(a),
#     data = pl.DataFrame(var_dic)
#     print("len = ", len(test_case))
#     for i in range(len(test_case)):
#         if i == 14:
#             continue
#         test_result = test_pp.parser(test_case[i])
#         objective_result = data.select(
#             test_result.alias("result")
#         ).to_numpy()
#         h = np.hstack(objective_result )
#         #print("h=",h)
#         #print('objective=', objective_result)
#         for j in range(len(h)): 
#             if math.isclose( h[j],expected[i][j],rel_tol=1e-5): 
#                 print("error at: ", test_case[i])
#     print ("done")
#        np.ceil(x1),
#         np.floor(x1),
#         np.max(a),
#         np.min(a),
#         np.sum(a),
#         np.product(a),
#     ]
#     test_pp = pp.parser_polars()
#     test_case = TEST_CASES
#     var_dic = {"A":a,"B":b,"X":x1}
#     data = pl.DataFrame(var_dic)
#     print("len = ", len(test_case))
#     for i in range(len(test_case)):
#         if i == 14:
#             continue
#         test_result = test_pp.parser(test_case[i])
#         objective_result = data.select(
#             test_result.alias("result")
#         ).to_numpy()
#         h = np.hstack(objective_result )
#         #print("h=",h)
#         #print('objective=', objective_result)
#         for j in range(len(h)): 
#             if math.isclose( h[j],expected[i][j],rel_tol=1e-5): 
#                 print("error at: ", test_case[i])
#     print ("done")
        
        

#test simple expresion with one operator