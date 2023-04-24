
class parser_numexpr:
    operator_map = {
        #Relational Operators
        "Equal":"==",
        "Greater":">",
        "GreaterEqual":">=",
        "Less":"<",
        "LessEqual":"<=",
        "NotEqual":"!=",

        #Functions
        "Add":"+",
        "Substract":"-",
        "Negate":"-",
        "Multiply":"*",
        "Divide":"/",
        "Power":"**",
    }
    function_map = {
        "Sqrt":"sqrt",
        "Exp":"exp",
        "Expm1":"expm1",
        #Rounding
        "Abd": "abs",

        #Trigonometry
        "Sin": "sin",
        "Cos":"cos",
        "Tan":"tan",
        "Arcsin":"arcsin",
        "Arccos":"arccos",
        "Arctan":"arctan",
        "Arctan2":"Arctan2",
        "Sinh":"sinh",
        "Cosh":"cosh",
        "Tanh":"tanh",
        "Arcsinh":"arcsinh",
        "Arcosh":"arcosh",
        "Artanh":"artanh",

        #Transcendental Functions
        "Exp":"exp",
        "Ln": "log",
        "Lg": "log10",
        "LogOnePlus": "log1p",
    }

    expr = {
        "Operator": operator_map,
        "Function": function_map
    }

    # convert math json into 1 dimenstion list 
    # ex: ["Multiply",["Sqrt","B"],["Power", "A","B"] ] -> ["Multiply","Sqrt","B","Power", "A","B" ]
    expression = []
    def decompose_list(self,l):
        for i in l:
            item_type = type(i)
            if item_type == list:
                self.decompose_list(self,i)
            else:
                self.expression.append(i)
    
    def parser(self, math_json):
        stack = []
        self.decompose_list(math_json)
        print(self.expression)
        expr_list = list(reversed(self.expression))
        for i in expr_list:
            if i in self.expr["Operator"]:
                p = self.expr["Operator"][i]
                op1 = stack.pop ()
                op2 = stack.pop ()
                stack.append ('(%s %s %s)' % (op1, p, op2) )
            elif i in self.expr["Function"]:
                p = self.expr["Function"][i]
                op = stack.pop ()
                stack.append ('%s(%s)' % (p, op) )
            else:
                stack.append (i)
        return stack.pop()

