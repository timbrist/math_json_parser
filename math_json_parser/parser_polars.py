import polars as pl
import math

#math json:
#https://cortexjs.io/compute-engine/guides/standard-library/
#polars expression:
#https://pola-rs.github.io/polars/py-polars/html/reference/expressions/index.html
class parser_polars:
    operators = {
        #MAX, MIN
        "Max":                    lambda x: pl.Expr.max(x),
        "Min":                    lambda x: pl.Expr.min(x),
        #SUM,PRODUCT OPERATION
        "Sum":                    lambda x: pl.Expr.sum(x),
        "Product":                lambda x: pl.Expr.product(x),
    }
    constants = {
        "ExponentialE":math.e,
        "pi": math.pi,
        "Pi": math.pi,
        "e":math.e,
        "Degree": math.pi/180,
    }
    relational_operators = {
        #BOOL OPERATION
        "Equal":                 lambda a,b: a == b,#0
        "Greater":               lambda a,b: a >  b,
        "GreaterEqual":          lambda a,b: a >= b,
        "Less":                  lambda a,b: a <  b,
        "LessEqual":             lambda a,b: a <= b,
        "NotEqual":              lambda a,b: a != b,#5
    }
    functions = {
        #BASIC OPERATION
        "Add":                   lambda a,b: a +  b,#6
        "Substract":             lambda a,b: a -  b,
        "Negate":                lambda a  :     -a,
        "Multiply":              lambda a,b: a *  b,
        "Divide":                lambda a,b: a /  b,
        "Power":                 lambda a,b: a ** b,
        "Root":                  lambda a,b: a **(1/b),
        "Sqrt":                  lambda a  : a **(1/2),#12
        "Squre":                 lambda a  : a **(2),
    } 
    transcendental_functions = {
        #EXPONENTS AND LOGARITHMS
        "Exp":                    lambda x: pl.Expr.exp(x),
        "Ln":                     lambda x: pl.Expr.log(x),#30
        "Log":                    lambda x,base: pl.Expr.log(x,base=base),#base must be a number
        "Lb":                     lambda x: pl.Expr.log(x,2),
        "Lg":                     lambda x: pl.Expr.log10(x),
        "LogOnePlus":             lambda x: pl.Expr.log1p(x),        
    }
    rounding = {
        #ROUDING OPERATION
        "Abs":                    lambda x: pl.Expr.abs(x),       
        "Ceil":                   lambda x: pl.Expr.ceil(x),# 
        "Floor":                  lambda x: pl.Expr.floor(x),#35 
    }
    trigonometric_functions = {
        #TRIGONOMETRIC OPERATION
        "Approch_Unique":         lambda x: pl.Expr.approx_unique(x),#15
        "Arccos":                 lambda x: pl.Expr.arccos(x),#  x ∊ [−1, 1] 
        "Arccosh":                lambda x: pl.Expr.arccosh(x),
        "Arcsin":                 lambda x: pl.Expr.arcsin(x),# x ∊ [−1, 1] 
        "Arcsinh":                lambda x: pl.Expr.arcsinh(x),
        "Arctan":                 lambda x: pl.Expr.arctan(x),#
        "Arctanh":                lambda x: pl.Expr.arctanh(x),# x ∊ (−INF,1] and [1,INF)
        "Arg_Unique":             lambda x: pl.Expr.arg_unique(x),
        "Cos":                    lambda x: pl.Expr.cos(x),
        "Cosh":                   lambda x: pl.Expr.cosh(x),
        "Sin":                    lambda x: pl.Expr.sin(x),
        "Sinh":                   lambda x: pl.Expr.sinh(x),
        "Tan":                    lambda x: pl.Expr.tan(x),
        "Tanh":                   lambda x: pl.Expr.tanh(x),
    }


    def parser(self,textlist):
        try:
            if isinstance(textlist, list):
                operator = textlist[0]
                parameter_len =  len(textlist[1:])  
                #iterate all the dictionaries
                for d in [self.operators,self.relational_operators,
                        self.functions,self.transcendental_functions,
                        self.rounding,self.trigonometric_functions]:
                    #if the operator is found in a dictionary, parse it.
                    if operator in d: 
                        if parameter_len == 1:
                            return d[operator](self.parser(textlist[1]))
                        elif parameter_len == 2:
                            return d[operator](self.parser(textlist[1]), self.parser(textlist[2]))
                        else:
                            print("number of parameter is exceed")
            #if the element is a constant than it should just return the number
            elif isinstance(textlist, (int, float, complex) ):
                return textlist
            #if the element is common math simbol than it should return the constant number.
            elif textlist in self.constants:
                return self.constants[textlist]
            #if the element is variable than use polars col.
            else:
                return pl.col(textlist) 
        except Exception as err:
            print(f"Unexpected {err=}, {type(err)=}")
            raise
       
