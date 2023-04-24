# math_json_parser
parse MathJson in python, polars expression, numpy expression,

Given any input follows MathJson formats,
["Multiply", "A", "Pi"]
["Exp", ["Multiply", "ImaginaryUnit", "Pi"]]
Give the output as polars expression, numpy expression, both can be evaluate. 
A*Pi
e**j*Pi
