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

@pytest.fixture
def simple_expr():
    #one operator test case
    test_json_case = [
        ["Equal","A","B"],
        ["Greater","A","B"],
        ["GreaterEqual","A","B"],
        ["Less","A","B"],
        ["LessEqual","A","B"],#5
        ["NotEqual","A","B"],
        ["Add","A","B"],
        ["Substract","A","B"],
        ["Negate","A"],
        ["Multiply","A","B"],
        ["Divide","A","B"],
        ["Power","A","B"],
        ["Sqrt","A"],
        ["Abs","A"],
        ["Approch_Unique","A"],
        ["Arccos","A"],
        ["Arccosh","A"],
        ["Arcsin","A"],
        ["Arcsinh","A"],
        ["Arctan","A"],
        ["Arctanh","A"],
        ["Arg_Unique","A"],
        ["Cos","A"],
        ["Cosh","A"],
        ["Sin","A"],
        ["Sinh","A"],
        ["Tan","A"],
        ["Tanh","A"],
        ["Exp","A"],
        ["Ln","A"],
        ["Log2","A"],
        ["Lg","A"],
        ["LogOnePlus","A"],
        ["Ceil","A"],
        ["Floor","A"],
        ["Max","A"],
        ["Min","A"],
        ["Sum","A"],
        ["Product","A"], 
    ]
    excepted_result =[
        str(pl.col("A") == pl.col("B")),
        str(pl.col("A") > pl.col("B")),
        str(pl.col("A") >= pl.col("B")),
        str(pl.col("A") < pl.col("B")),
        str(pl.col("A") <= pl.col("B")),
        str(pl.col("A") != pl.col("B")),
        str(pl.col("A") + pl.col("B")),
        str(pl.col("A") - pl.col("B")),
        str(-pl.col("A")),
        str(pl.col("A") * pl.col("B")),
        str(pl.col("A") / pl.col("B")),
        str(pl.col("A") ** pl.col("B")),
        str(pl.col("A") ** (1/2)),

        str(pl.col("A").abs()),
        str(pl.col("A").approx_unique()),
        str(pl.col("A").arccos()),
        str(pl.col("A").arccosh()),
        str(pl.col("A").arcsin()),
        str(pl.col("A").arcsinh()),
        str(pl.col("A").arctan()),
        str(pl.col("A").arctanh()),
        str(pl.col("A").arg_unique()),
        str(pl.col("A").cos()),
        str(pl.col("A").cosh()),
        str(pl.col("A").sin()),
        str(pl.col("A").sinh()),
        str(pl.col("A").tan()),
        str(pl.col("A").tanh()),
        str(pl.col("A").exp()),
        str(pl.col("A").log()),
        str(pl.col("A").log(base=2)),
        str(pl.col("A").log10()),
        str(pl.col("A").log1p()),
        str(pl.col("A").ceil()),
        str(pl.col("A").floor()),
        str(pl.col("A").max()),
        str(pl.col("A").min()),
        str(pl.col("A").sum()),
        str(pl.col("A").product()), 
    ]
    return test_json_case, excepted_result


#test simple expresion with one operator
def test_simple_expr(simple_expr):
    test_case, result = simple_expr
    test_pp = pp.parser_polars()
    for i in range(len(test_case)):
        test_result = test_pp.parser(test_case[i])
        assert str(test_result) == result[i]