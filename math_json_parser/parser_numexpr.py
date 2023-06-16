import math

#math json:
#https://cortexjs.io/compute-engine/guides/standard-library/
#numpy expression:
#https://pandas.pydata.org/docs/user_guide/enhancingperf.html#enhancingperf-eval
class parser_numexpr:
    operators = {
        #Pandas.eval() hasn't support the following operation yet.
        #MAX, MIN
        #"Max":                    lambda x: "max(%s)" % x,
        #"Min":                    lambda x: "min(%s)" % x,
        #SUM,PRODUCT OPERATION
        #"Sum":                    lambda x: "sum(%s)" % x,
        #"Product":                lambda x: "prod(%s)" % x,
    }
    relational_operators = {
        #BOOL OPERATION
        "Equal":                 lambda a,b: '(%s == %s)' % (a, b),  
        "Greater":               lambda a,b: '(%s >  %s)' % (a, b),
        "GreaterEqual":          lambda a,b: '(%s >= %s)' % (a, b),
        "Less":                  lambda a,b: '(%s <  %s)' % (a, b),
        "LessEqual":             lambda a,b: '(%s <= %s)' % (a, b),
        "NotEqual":              lambda a,b: '(%s != %s)' % (a, b),
    }
    functions = {
        #BASIC OPERATION
        "Add":                   lambda a,b: '(%s +  %s)' % (a, b),
        "Substract":             lambda a,b: '(%s -  %s)' % (a, b),
        "Negate":                lambda a: '(-%s)' % a,
        "Multiply":              lambda a,b: '(%s *  %s)' % (a, b),
        "Divide":                lambda a,b: '(%s /  %s)' % (a, b),
        "Power":                 lambda a,b: '(%s ** %s)' % (a, b),
        "Root":                  lambda a,b: '(%s ** (1/%s))' % (a, b),
        "Sqrt":                  lambda a  : '(%s ** (1/2))' % a,
        "Squre":                 lambda a  : '(%s ** (2))'  % a,
    } 
    transcendental_functions = {
        #EXPONENTS AND LOGARITHMS
        "Exp":                   lambda a: 'exp(%s)' % (a),
        "Ln":                    lambda a: 'log(%s)' % (a),
        "Log":                   lambda a,b: 'log(%s,%s)' % (a,b),
    #    "Lb":                    lambda a: 'log(%s,2)'% a,
        "Lg":                    lambda a: 'log10(%s)' % (a),
        "LogOnePlus":            lambda a: 'log1p(%s)' % (a),      
    }
    rounding = {
        #ROUDING OPERATION
        "Abs":                   lambda a: 'abs(%s)' % (a),       
    }
    trigonometric_functions = {
        #TRIGONOMETRIC OPERATION

        "Sin":                   lambda a: 'sin(%s)' % (a),
        "Cos":                   lambda a: 'cos(%s)' % (a),
#        "Tan":                   lambda a: 'tan(%s)' % (a),
        "Arcsin":                lambda a: 'arcsin(%s)' % (a),#∀ x ∊ [ − 1 , 1 ] 
        "Arccos":                lambda a: 'arccos(%s)' % (a),
        "Arctan":                lambda a: 'arctan(%s)' % (a), #∀ x ∊ ( − 1 , 1 ) 
        "Sinh":                  lambda a: 'sinh(%s)' % (a),
        "Cosh":                  lambda a: 'cosh(%s)' % (a),
        "Tanh":                  lambda a: 'tanh(%s)' % (a),
        "Arcsinh":               lambda a: 'arcsinh(%s)' % (a),
        "Arccosh":               lambda a: 'arccosh(%s)' % (a),#∀x >= 1 ,
        "Arctanh":               lambda a: 'arctanh(%s)' % (a), 
        "Arctan2":               lambda a,b: 'arctan2(%s,%s)' % (a,b),

    }
    constants = {
        "ExponentialE":math.e,
        "pi": math.pi,
        "Pi": math.pi,
        "e":math.e,
        "Degree": math.pi/180,
    }

    def __init__(self) -> None:
        self.numpy_expr = '' 
    def set_numpy_expr(self, __expr: str) -> None:
        self.numpy_expr = __expr
    def get_numpy_expr(self) -> str:
        return self.numpy_expr    

    def parser(self,textlist):
        try:
            if isinstance(textlist, str):
                return textlist
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
                self.set_numpy_expr(textlist)
                return self.get_numpy_expr()
        except Exception as err:
            print(f"Unexpected {err=}, {type(err)=}")
            raise

