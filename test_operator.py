from math_parser import MathParser 
import polars as pl
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
    elif textlist == "ImaginaryUnit":
        #cons_dict["ImaginaryUnit"] = math.pi
        return pl.col(textlist)
    raise ValueError

math_json = ["Add", ["Sin",  ["Substract","Pi","B"]], \
        ["Multiply", ["Sqrt","B"], ["Power", "A","B"] ]  ]
# print(math_json[::-1])
func1 = parse(math_json)

func2 = parse(["Multiply", "A", "Pi"])

func3 = parse(json_array["fn3"])

print("The custom function is", func3)
var_dict = {"A": [20, 30], "B":[5, 7]}
var_dict.update(cons_dict)
data = pl.DataFrame(var_dict)
objectives = data.select(
    func1.alias("Objective 1"),
    func2.alias("Objective 2"),
)
data2 = pl.DataFrame(cons_dict)
objectives2 = data2.select(
    func3.alias("f3")   
)
print("The output is", objectives2)