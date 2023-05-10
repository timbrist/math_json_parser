# Math Json Parser

## Abtract
Math Json Parser aim to convert mathematical notation in json to 
expressions of well know python library: polars, numpy; 

## Background
Math Json: https://cortexjs.io/math-json/ \\
Polars Expression: https://pola-rs.github.io/polars/py-polars/html/reference/expressions/index.html \\
numpy expression in pandas: https://pandas.pydata.org/docs/reference/api/pandas.DataFrame.eval.html \\

## Example
input_json = ["Multiply", ["Add","A","B"],"A"] \\
output_json = math_json_parser.parser_polars.parser(input_json) \\
output_json > " (col("A")+col("B") ) * col("A") " \\

## Installation
- you can just copy past math_json_parser to your project and import it.\\
- use poetry intall to set up development environments.\\
1. `git clone https://github.com/timbrist/math_json_parser.git`
2. `cd math_json_parser`
4. `poetry install`

