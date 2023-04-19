from math_parser import MathParser 
import polars as pl

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
    raise ValueError

math_json = ["Add", ["Sqrt",  ["Substract","A","B"]], \
        ["Multiply", ["Sqrt","B"], ["Power", "A","B"] ]  ]
# print(math_json[::-1])
func1 = parse(math_json)

func2 = parse(["Multiply", "A", "B"])

print("The custom function is", func1)
print("type: ", type(func1))
data = pl.DataFrame({"A": [20, 30], "B":[5, 7]})

objectives = data.select(
    func1.alias("Objective 1"),
    func2.alias("Objective 2")
)

print("The output is", objectives)