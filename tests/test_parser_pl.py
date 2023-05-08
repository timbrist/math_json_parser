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
        ["LessEqual","A","B"],
        ["NotEqual","A","B"],
]
FUNCTION_CASES = [
        ["Add","A","B"],
        ["Substract","A","B"],
        ["Negate","A"],
        ["Multiply","A","B"],
        ["Divide","A","B"],
        ["Power","A","B"],
        ["Root","A","B"],
        ["Sqrt","A"],
        ["Squre","A"],
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
        ["Ceil","A"],
        ["Floor","A"],
]
TRIGONOMETRIC_CASES = [
        ["Arccos","X"],
        ["Arccosh","X1"],
        ["Arcsin","X"],
        ["Arcsinh","X"],
        ["Arctan","X"],#20
        ["Arctanh","X"],
        ["Cos","X"],
        ["Cosh","X"],
        ["Sin","X"],#25
        ["Sinh","X"],
        ["Tan","X"],
        ["Tanh","X"],
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
        str(pl.col("A") ** (1/pl.col("B"))),
        str(pl.col("A") ** (1/2)),
        str(pl.col("A") ** (2)),
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
        str(pl.col("A").ceil()),
        str(pl.col("A").floor()),
    ]
    excepted_trigonometric =[
        str(pl.col("X").arccos()),
        str(pl.col("X1").arccosh()),
        str(pl.col("X").arcsin()),
        str(pl.col("X").arcsinh()),
        str(pl.col("X").arctan()),
        str(pl.col("X").arctanh()),
        str(pl.col("X").cos()),
        str(pl.col("X").cosh()),
        str(pl.col("X").sin()),
        str(pl.col("X").sinh()),
        str(pl.col("X").tan()),
        str(pl.col("X").tanh()),
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


def test_simple_operators():
    a = np.random.randint(100,size=(5))
    expected = [
        np.max(a),
        np.min(a),
        np.sum(a),
        np.prod(a),
    ]
    var_dic = {"A":a}
    data = pl.DataFrame(var_dic)
    test_pp = pp.parser_polars()
    for i in range(len(OPERATROS_CASES)):
        test_result = test_pp.parser(OPERATROS_CASES[i])
        objective_result = data.select(
            test_result.alias("result")
        ).to_numpy()
        h = np.hstack(objective_result )
        for j in range(len(h)): 
            assert math.isclose( h[j], expected[i],rel_tol=1e-5)

def test_simple_relational():
    a = np.random.randint(100,size=(5))
    b = np.random.randint(100,size=(5))
    expected = [
        a == b,
        a >  b,
        a >= b,
        a <  b,
        a <= b,
        a != b,
    ]
    var_dic = {"A":a,"B":b}
    data = pl.DataFrame(var_dic)
    test_pp = pp.parser_polars()
    for i in range(len(RELATIONAL_CASES)):
        test_result = test_pp.parser(RELATIONAL_CASES[i])
        objective_result = data.select(
            test_result.alias("result")
        ).to_numpy()
        h = np.hstack(objective_result )
        for j in range(len(h)): 
            assert h[j] == expected[i][j]

def test_simple_functions():
    a = np.random.randint(1,10,size=(5))
    b = np.random.randint(1,10,size=(5))
    expected = [
        a +  b,
        a -  b,
        -a,
        a *  b,
        a /  b,
        a ** b,
        a ** (1/b),
        a ** (1/2),
        a **(2),
    ]
    var_dic = {"A":a,"B":b}
    data = pl.DataFrame(var_dic)
    test_pp = pp.parser_polars()
    for i in range(len(FUNCTION_CASES)):
        test_result = test_pp.parser(FUNCTION_CASES[i])
        objective_result = data.select(
            test_result.alias("result")
        ).to_numpy()
        h = np.hstack(objective_result )
        for j in range(len(h)): 
            print(h[j], expected[i][j])
            print(FUNCTION_CASES[i])
            assert math.isclose( h[j], expected[i][j],rel_tol=1e-5)

def test_simple_transcendental():
    a = np.random.randint(1,100,size=(5))
    expected = [
        np.exp(a),
        np.log(a),
        np.emath.logn(4, a),
        np.emath.logn(2, a),
        np.log10(a),
        np.log1p(a),
    ]
    var_dic = {"A":a}
    data = pl.DataFrame(var_dic)
    test_pp = pp.parser_polars()
    for i in range(len(TRANSCENDENTAL_CASES)):
        test_result = test_pp.parser(TRANSCENDENTAL_CASES[i])
        objective_result = data.select(
            test_result.alias("result")
        ).to_numpy()
        h = np.hstack(objective_result )
        for j in range(len(h)): 
            print(h[j], expected[i][j])
            print(TRANSCENDENTAL_CASES[i])
            assert math.isclose( h[j], expected[i][j],rel_tol=1e-5)


def test_simple_rounding():
    a = np.random.uniform(100,size=(5))
    expected = [
        np.absolute(a),
        np.ceil(a),
        np.floor(a),
    ]
    var_dic = {"A":a}
    data = pl.DataFrame(var_dic)
    test_pp = pp.parser_polars()
    for i in range(len(ROUNDING_CASES)):
        test_result = test_pp.parser(ROUNDING_CASES[i])
        objective_result = data.select(
            test_result.alias("result")
        ).to_numpy()
        h = np.hstack(objective_result )
        for j in range(len(h)): 
            print(h[j], expected[i][j])
            print(ROUNDING_CASES[i])
            assert math.isclose( h[j], expected[i][j],rel_tol=1e-5)

def test_simple_trigonometric():
    x = np.random.uniform(-1,1,size=(5))
    x1 = np.random.uniform(1,100,size=(5))
    expected = [
        np.arccos(x),
        np.arccosh(x1),
        np.arcsin(x),
        np.arcsinh(x),
        np.arctan(x),
        np.arctanh(x),
        np.cos(x),
        np.cosh(x),
        np.sin(x),
        np.sinh(x),
        np.tan(x),
        np.tanh(x),
    ]
    var_dic = {"X":x,"X1":x1}
    data = pl.DataFrame(var_dic)
    test_pp = pp.parser_polars()
    for i in range(len(TRIGONOMETRIC_CASES)):
        test_result = test_pp.parser(TRIGONOMETRIC_CASES[i])
        objective_result = data.select(
            test_result.alias("result")
        ).to_numpy()
        h = np.hstack(objective_result )
        for j in range(len(h)): 
            print(h[j], expected[i][j])
            print(TRIGONOMETRIC_CASES[i])
            assert math.isclose( h[j], expected[i][j],rel_tol=1e-5)
