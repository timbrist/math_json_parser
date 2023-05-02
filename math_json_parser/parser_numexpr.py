class parser_numexpr:
    operator_map = {
        #Relational Operators
        "Equal":                 lambda a,b: '(%s == %s)' % (a, b),  
        "Greater":               lambda a,b: '(%s >  %s)' % (a, b),
        "GreaterEqual":          lambda a,b: '(%s >= %s)' % (a, b),
        "Less":                  lambda a,b: '(%s <  %s)' % (a, b),
        "LessEqual":             lambda a,b: '(%s <= %s)' % (a, b),
        "NotEqual":              lambda a,b: '(%s != %s)' % (a, b),
        #Functions
        "Add":                   lambda a,b: '(%s +  %s)' % (a, b),
        "Substract":             lambda a,b: '(%s -  %s)' % (a, b),
        "Negate":                lambda a,b: '(%s -  %s)' % (a, b),
        "Multiply":              lambda a,b: '(%s *  %s)' % (a, b),
        "Divide":                lambda a,b: '(%s /  %s)' % (a, b),
        "Power":                 lambda a,b: '(%s ** %s)' % (a, b),
        "Arctan2":               lambda a,b: 'arctan2(%s,%s)' % (a,b), #math.atan2(x,y) 
        "Sqrt":                  lambda a: 'sqrt(%s)' % (a), 
        "Expm1":                 lambda a: 'expm1(%s)' % (a),
        "Abs":                   lambda a: 'abs(%s)' % (a), 
        "Sin":                   lambda a: 'sin(%s)' % (a),
        "Cos":                   lambda a: 'cos(%s)' % (a),
        "Tan":                   lambda a: 'tan(%s)' % (a),
        "Arcsin":                lambda a: 'arcsin(%s)' % (a),#∀ x ∊ [ − 1 , 1 ] 
        "Arccos":                lambda a: 'arccos(%s)' % (a),
        "Arctan":                lambda a: 'arctan(%s)' % (a), #∀ x ∊ ( − 1 , 1 ) 
        "Sinh":                  lambda a: 'sinh(%s)' % (a),
        "Cosh":                  lambda a: 'cosh(%s)' % (a),
        "Tanh":                  lambda a: 'tanh(%s)' % (a),
        "Arcsinh":               lambda a: 'arcsinh(%s)' % (a),
        "Arccosh":               lambda a: 'arccosh(%s)' % (a),#∀x >= 1 ,
        "Arctanh":               lambda a: 'arctanh(%s)' % (a), 
        "Exp":                   lambda a: 'exp(%s)' % (a),
        "Ln":                    lambda a: 'log(%s)' % (a),
        "Lg":                    lambda a: 'log10(%s)' % (a),
        "LogOnePlus":            lambda a: '10g1p(%s)' % (a),
    }
    def __init__(self) -> None:
        self.numpy_expr = '' 
    def set_numpy_expr(self, __expr: str) -> None:
        self.numpy_expr = __expr
    def get_numpy_expr(self) -> str:
        return self.numpy_expr    

    def parser2(self,textlist):
        if isinstance(textlist, list):
            operator = textlist[0]
            parameter_len =  len(textlist[1:]) 
            if parameter_len == 1:
                return self.operator_map[operator](self.parser2(textlist[1]))
            elif parameter_len == 2:
                return self.operator_map[operator](self.parser2(textlist[1]), self.parser2(textlist[2]))
            else:
                print("number of parameter is exceed")
        elif textlist not in self.operator_map:
            self.set_numpy_expr(textlist)
            return self.get_numpy_expr()
        raise ValueError

