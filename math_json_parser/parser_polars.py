import polars as pl


#polars expression:
#https://pola-rs.github.io/polars/py-polars/html/reference/expressions/computation.html
class parser_polars:
    operator_map = {
        "Equal":                 lambda a,b: a == b,  
        "Greater":               lambda a,b: a >  b,
        "GreaterEqual":          lambda a,b: a >= b,
        "Less":                  lambda a,b: a <  b,
        "LessEqual":             lambda a,b: a <= b,
        "NotEqual":              lambda a,b: a != b,
        "Add":                   lambda a,b: a +  b,
        "Substract":             lambda a,b: a -  b,
        "Negate":                lambda a,b: a -  b,
        "Multiply":              lambda a,b: a *  b,
        "Divide":                lambda a,b: a /  b,
        "Power":                 lambda a,b: a ** b,

        "Abs":                    lambda x: pl.Expr.abs(x),
        "Approch_Unique":         lambda x: pl.Expr.approx_unique(x),
        "Arccos":                 lambda x: pl.Expr.arccos(x),
        "Arccosh":                lambda x: pl.Expr.arccosh(x),
        "Arcsin":                 lambda x: pl.Expr.arcsin(x),
        "Arcsinh":                lambda x: pl.Expr.arcsinh(x),
        "Arctan":                 lambda x: pl.Expr.arctan(x),
        "Arctanh":                lambda x: pl.Expr.arctanh(x),
        "Arg_Unique":             lambda x: pl.Expr.arg_unique(x),
        "Cos":                    lambda x: pl.Expr.cos(x),
        "Cosh":                   lambda x: pl.Expr.cosh(x),
        "Exp":                    lambda x: pl.Expr.exp(x),
        "Ln":                     lambda x: pl.Expr.log(x),
        "Log":                    lambda x, base: pl.Expr.log(x,base),
        "Lg":                     lambda x: pl.Expr.log10(x),
        "LogOnePlus":             lambda x: pl.Expr.log1p(x),
        "Ceil":                   lambda x: pl.Expr.ceil(x),
        "Floor":                  lambda x: pl.Expr.floor(x),
        "Sin":                    lambda x: pl.Expr.sin(x),
        "Sinh":                   lambda x: pl.Expr.sinh(x),
        "Tan":                    lambda x: pl.Expr.tan(x),
        "Tanh":                   lambda x: pl.Expr.tanh(x),
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
        elif textlist not in self.operator_map:
            return pl.col(textlist)
        raise ValueError

