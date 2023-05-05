import polars as pl
import math

#polars expression:
#https://pola-rs.github.io/polars/py-polars/html/reference/expressions/computation.html
class parser_polars:
    operator_map = {
        "Equal":                 lambda a,b: a == b,  
        "Greater":               lambda a,b: a >  b,
        "GreaterEqual":          lambda a,b: a >= b,
        "Less":                  lambda a,b: a <  b,
        "LessEqual":             lambda a,b: a <= b,#5
        "NotEqual":              lambda a,b: a != b,
        "Add":                   lambda a,b: a +  b,
        "Substract":             lambda a,b: a -  b,
        "Negate":                lambda a  :     -a,
        "Multiply":              lambda a,b: a *  b,#10
        "Divide":                lambda a,b: a /  b,
        "Power":                 lambda a,b: a ** b,
        "Sqrt":                  lambda a  : a **(1/2),

        "Abs":                    lambda x: pl.Expr.abs(x),
        "Approch_Unique":         lambda x: pl.Expr.approx_unique(x),
        "Arccos":                 lambda x: pl.Expr.arccos(x),#15
        "Arccosh":                lambda x: pl.Expr.arccosh(x),
        "Arcsin":                 lambda x: pl.Expr.arcsin(x),
        "Arcsinh":                lambda x: pl.Expr.arcsinh(x),
        "Arctan":                 lambda x: pl.Expr.arctan(x),
        "Arctanh":                lambda x: pl.Expr.arctanh(x),#20
        "Arg_Unique":             lambda x: pl.Expr.arg_unique(x),
        "Cos":                    lambda x: pl.Expr.cos(x),
        "Cosh":                   lambda x: pl.Expr.cosh(x),
        "Sin":                    lambda x: pl.Expr.sin(x),
        "Sinh":                   lambda x: pl.Expr.sinh(x),
        "Tan":                    lambda x: pl.Expr.tan(x),
        "Tanh":                   lambda x: pl.Expr.tanh(x),
        "Exp":                    lambda x: pl.Expr.exp(x),
        "Ln":                     lambda x: pl.Expr.log(x),
        "Log2":                    lambda x: pl.Expr.log(x,2),
        "Lg":                     lambda x: pl.Expr.log10(x),
        "LogOnePlus":             lambda x: pl.Expr.log1p(x),
        "Ceil":                   lambda x: pl.Expr.ceil(x),
        "Floor":                  lambda x: pl.Expr.floor(x),
        "Max":                    lambda x: pl.Expr.max(x),
        "Min":                    lambda x: pl.Expr.min(x),
        "Sum":                    lambda x: pl.Expr.sum(x),
        "Product":                lambda x: pl.Expr.product(x),
    }
    constant_map = {
        "pi": math.pi,
        "Pi": math.pi,
        "e":math.e,
    }
    def parser(self,textlist):
        if isinstance(textlist, list):
            operator = textlist[0]
            parameter_len =  len(textlist[1:]) 
            if parameter_len == 1:
                return self.operator_map[operator](self.parser(textlist[1]))
            elif parameter_len == 2:
                return self.operator_map[operator](self.parser(textlist[1]), self.parser(textlist[2]))
            else:
                print("number of parameter is exceed")
        #if the element is a constant than it should just return the number
        elif isinstance(textlist, (int, float, complex) ):
            return textlist
        #if the element is common math simbol than it should return the constant number.
        elif textlist in self.constant_map:
            return self.constant_map[textlist]
        #if the element is variable than use polars col.
        else:
            return pl.col(textlist) 
        raise ValueError

