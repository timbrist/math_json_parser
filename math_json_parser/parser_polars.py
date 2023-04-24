import polars as pl

class parser_polars:
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

