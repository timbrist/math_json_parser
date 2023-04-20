
class MathParser:
    operator_map = {
        #Relational Operators
        "Equal":"==",
        "Greater":">",
        "GreaterEqual":">=",
        "Less":"<",
        "LessEqual":"<=",
        "NotEqual":"!=",

        #Functions
        "Add":"+",
        "Substract":"-",
        "Negate":"-",
        "Multiply":"*",
        "Divide":"/",
        "Power":"**",
    }
    function_map = {
        "Sqrt":"sqrt",
        "Exp":"exp",
        "Expm1":"expm1",
        #Rounding
        "Abd": "abs",

        #Trigonometry
        "Sin": "sin",
        "Cos":"cos",
        "Tan":"tan",
        "Arcsin":"arcsin",
        "Arccos":"arccos",
        "Arctan":"arctan",
        "Arctan2":"Arctan2",
        "Sinh":"sinh",
        "Cosh":"cosh",
        "Tanh":"tanh",
        "Arcsinh":"arcsinh",
        "Arcosh":"arcosh",
        "Artanh":"artanh",

        #Transcendental Functions
        "Exp":"exp",
        "Ln": "log",
        "Lg": "log10",
        "LogOnePlus": "log1p",
    }

    expr = {
        "Operator": operator_map,
        "Function": function_map
    }



import json
print("Hello world")
input_file = open ('test_data.json')
json_array = json.load(input_file)

# 1, push every element into a list
expression = []
def decompose_list(l):
    for i in l:
        item_type = type(i)
        if item_type == list:
            decompose_list(i)
        else:
            expression.append(i)

decompose_list(json_array['fn3'])
print(expression)

def parser(expr_list):
    stack = []
    for i in list(reversed( expr_list)):
        if i in MathParser.expr["Operator"]:
            p = MathParser.expr["Operator"][i]
            op1 = stack.pop ()
            op2 = stack.pop ()
            stack.append ('(%s %s %s)' % (op1, p, op2) )
        elif i in MathParser.expr["Function"]:
            p = MathParser.expr["Function"][i]
            op = stack.pop ()
            stack.append ('%s(%s)' % (p, op) )
        else:
            stack.append (i)
    return stack.pop()


import numexpr as ne
import math
ImaginaryUnit = complex(0,1)
Pi = math.pi
expr = parser(expression)
print(expr)
print(ne.evaluate(expr))