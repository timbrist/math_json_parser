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
import math_json_parser.parser_numexpr as pe
import pytest
import numpy as np
import pandas as pd

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
        ["Ln","A"],
        ["Log","A","B"],
#        ["Lb","A"],
        ["Lg","A"],
        ["LogOnePlus","A"],
]
ROUNDING_CASES = [
        ["Abs","A"],
]
TRIGONOMETRIC_CASES = [
        ["Sin","X"],
        ["Cos","X"],
#        ["Tan","X"],
        ["Arcsin","X"],
        ["Arccos","X"],
        ["Arctan","X"],
        ["Sinh","X"],
        ["Cosh","X"],
        ["Tanh","X"],
        ["Arcsinh","X"],
        ["Arccosh","X1"],
        ["Arctanh","X"],
        ["Arctan2","X","X1"],

]


def test_randomly():
    test_json = ["Add",["Multiply","A","B"],"A"]
    test_json2 = ['Sin',["Divide","A",["Cos","A"]]]
    test_ne = pe.parser_numexpr()
    test_result1 = test_ne.parser(test_json)
    test_result2 = test_ne.parser(test_json2)
    print(test_result1)
    print(test_result2)
    df = pd.DataFrame({'A': range(1, 6), 'B': range(10, 0, -2)})
    print(df.eval(test_result1))
    print(df.eval(test_result2))

def test_simple_relational():
    a = np.random.randint(100,size=(5))
    b = np.random.randint(100,size=(5))
    var_dic = {"A":a,"B":b}
    df = pd.DataFrame(var_dic)
    expected = [
        df.eval("A==B"),
        df.eval("A>B"),
        df.eval("A>=B"),
        df.eval("A<B"),
        df.eval("A<=B"),
        df.eval("A!=B"),
    ]
    test_ne = pe.parser_numexpr()
    for i in range(len(RELATIONAL_CASES)):
        test_result = test_ne.parser(RELATIONAL_CASES[i])
        h =  df.eval(test_result)
        for j in range(len(h)):
            print(h[j], expected[i][j])
            print("AT: ",RELATIONAL_CASES[i])
            assert  h[j] == expected[i][j]


def test_simple_functions():
    a = np.random.randint(100,size=(5))
    b = np.random.randint(100,size=(5))
    var_dic = {"A":a,"B":b}
    df = pd.DataFrame(var_dic)
    expected = [
        df.eval("A+B"),
        df.eval("A-B"),
        df.eval("-A"),
        df.eval("A*B"),
        df.eval("A/B"),
        df.eval("A**B"),
        df.eval("A**(1/B)"),
        df.eval("A**(1/2)"),
        df.eval("A**(2)"),
    ]
    test_ne = pe.parser_numexpr()
    for i in range(len(FUNCTION_CASES)):
        test_result = test_ne.parser(FUNCTION_CASES[i])
        h =  df.eval(test_result)
        for j in range(len(h)):
            print(h[j], expected[i][j])
            print("AT: ",FUNCTION_CASES[i])
            assert math.isclose( h[j], expected[i][j],rel_tol=1e-5)

def test_simple_transcendental():
    a = np.random.randint(1,100,size=(5))
    b = np.random.randint(1,100,size=(5))
    var_dic = {"A":a,"B":b}
    df = pd.DataFrame(var_dic)
    expected = [
        df.eval("exp(A)"),
        df.eval("log(A)"),
        df.eval("log(A,B)"),
#       df.eval("log(A,2)"),
        df.eval("log10(A)"),
        df.eval("log1p(A)"),
    ]
    test_ne = pe.parser_numexpr()
    for i in range(len(TRANSCENDENTAL_CASES)):
        test_result = test_ne.parser(TRANSCENDENTAL_CASES[i])
        h =  df.eval(test_result)
        for j in range(len(h)):
            print(h[j], expected[i][j])
            print("AT: ",TRANSCENDENTAL_CASES[i])
            assert math.isclose( h[j], expected[i][j],rel_tol=1e-5)


def test_simple_trigonometric():
    x = np.random.uniform(-1,1,size=(5))
    x1 = np.random.uniform(1,100,size=(5))
    var_dic = {"X":x,"X1":x1}
    df = pd.DataFrame(var_dic)
    expected = [
        df.eval("sin(X)"),
        df.eval("cos(X)"),
        #df.eval("tan(X)"),
        df.eval("arcsin(X)"),
        df.eval("arccos(X)"),
        df.eval("arctan(X)"),
        df.eval("sinh(X)"),
        df.eval("cosh(X)"),
        df.eval("tanh(X)"),
        df.eval("arcsinh(X)"),
        df.eval("arccosh(X1)"),
        df.eval("arctanh(X)"),
        df.eval("arctan2(X,X1)"),
    ]
    test_ne = pe.parser_numexpr()
    for i in range(len(TRIGONOMETRIC_CASES)):
        test_result = test_ne.parser(TRIGONOMETRIC_CASES[i])
        h =  df.eval(test_result)
        for j in range(len(h)):
            print(h[j], expected[i][j])
            print("AT: ",TRIGONOMETRIC_CASES[i])
            assert math.isclose( h[j], expected[i][j],rel_tol=1e-5)

