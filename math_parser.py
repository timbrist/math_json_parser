
import math

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

    def sin(x):
        return math.sin(x)
    operator_map = {
        #Constants 
        "ExponentialE":math.e,
        "ImaginaryUnit": complex(0,1), # TODO: complex number 
        "MachineEpsilon": "2**(-52)",

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
        "Exp":lambda x: math.exp(x),
        "Ln": lambda x: math.log(x),
        "Log": lambda x, base: math.log(x,base),
        "Lb": lambda x: math.log2(x),
        "Lg": lambda x: math.log10(x),
        "LogOnePlus": lambda x: math.log1p(x),

        #Rounding
        "Abd": lambda x: abs(x),
        "Ceil": lambda x: math.ceil(x),
        "Chop": "lambda x: chop(x)", #TODO: chop function
        "Floor": lambda x: math.floor(x),
        "Round": "lambda x: math.round(x)",#TODO:

        #Trigonometry
        "Degrees":math.degrees,
        "Pi":math.pi,
        "Sin": sin,
        "Cos":lambda x : math.cos(x),
        "Tan":lambda x : math.tan(x),
    }

print("Hello Operator Parser")