

import polars as pl

class MathParser:
    #Relational Operators
    def equal(x,y):
        return x == y
    def greater(x,y):
        return x > y
    def greater_equal(x,y):
        return x>=y
    def less(x,y):
        return x < y
    def less_equal(x,y):
        return x <= y
    def not_equal(x,y):
        return x!=y
    #Functions
    def add(a,b):
        return a + b
    def substract(a,b):
        return a - b
    def negate(a):
        return 0-a
    def multiply(a,b):
        return a * b
    def divide(a,b):
        try:
            return a/b
        except:
            print("exception: try to divide 0")
    def power(a,b):
        return a**b
    def root(x,n):
        return x**(1/n)

    operator_map = {

        #Relational Operators
        "Equal":equal,
        "Greater":greater,
        "GreaterEqual":greater_equal,
        "Less":less,
        "LessEqual":less_equal,
        "NotEqual":not_equal,

        #Functions
        "Add":add,
        "Substract":substract,
        "Negate":negate,
        "Multiply":multiply,
        "Divide":divide,
        "Power":power,
        "Root":root,
        "Sqrt":lambda x: x**(1/2),
        "Square":lambda x: x**2,

        #Transcendental Functions
        "Exp":lambda x: pl.Expr.exp(x),
        "Ln": lambda x: pl.Expr.log(x),
        "Log": lambda x, base: pl.Expr.log(x,base),
        #"Lb": lambda x: pl.Expr.log2(x),
        "Lg": lambda x: pl.Expr.log10(x),
        "LogOnePlus": lambda x: pl.Expr.log1p(x),

        #Rounding
        "Abd": lambda x: pl.Expr.abs(x),
        "Ceil": lambda x: pl.Expr.ceil(x),
        "Chop": "lambda x: chop(x)", #TODO: chop function
        "Floor": lambda x: pl.Expr.floor(x),
        "Round": "lambda x: pl.Expr.round(x)",#TODO:

        #Trigonometry
        #"Degrees":pl.Expr.degrees,
        "Sin": lambda x: pl.Expr.sin(x),
        "Cos":lambda x : pl.Expr.cos(x),
        "Tan":lambda x : pl.Expr.tan(x),
    }

import math
import json

input_file = open ('test_data.json')
json_array = json.load(input_file)

cons_dict = {}
# test_a = [1,2]
# print(MathParser.operator_map['Add'](*test_a))
# print(*test_a)
def parse(textlist):
    if isinstance(textlist, list):
        operator = textlist[0]
        parameter_len =  len(textlist[1:]) 
        if parameter_len == 1:
            return MathParser.operator_map[operator](parse(textlist[1]))
        elif parameter_len == 2:
            return MathParser.operator_map[operator](parse(textlist[1]), parse(textlist[2]))
        else:
            print("number of parameter is exceed")
    if textlist == "A" or textlist == "B":
        return pl.col(textlist)
    elif isinstance(textlist,(int, float)):
        cons_dict[str(textlist)] = textlist
        return pl.col(textlist)
    elif textlist == "Pi":
        cons_dict["Pi"] = math.pi
        return pl.col(textlist)
    raise ValueError

math_json = ["Add", ["Sin",  ["Substract","Pi","B"]], \
        ["Multiply", ["Sqrt","B"], ["Power", "A","B"] ]  ]
# print(math_json[::-1])
func1 = parse(math_json)

func2 = parse(["Multiply", "A", "Pi"])

func3 = parse(json_array["fn2"])

print("The custom function is", func3)
var_dict = {"A": [20, 30], "B":[5, 7]}
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

