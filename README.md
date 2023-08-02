# Math Json Parser

## Abtract
Math Json Parser aim to convert mathematical notation in json to 
expressions of well know python library: polars, numpy; 

## Background
Math Json: https://cortexjs.io/math-json/  
Polars Expression: https://pola-rs.github.io/polars/py-polars/html/reference/expressions/index.html   
numpy expression in pandas: https://pandas.pydata.org/docs/reference/api/pandas.DataFrame.eval.html  

## Example
expr = ["Multiply", ["Add","A","B"],"A"]  
output_json = math_parser.parse(expr)  
" (col("A")+col("B") ) * col("A") "  

## Installation
1. `git clone https://github.com/timbrist/math_json_parser.git`
2. `python MathParser.py`

