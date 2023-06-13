from desdeo_problem import Variable, ScalarObjective, ScalarConstraint, ScalarMOProblem
from parser_numexpr import parser_numexpr
import numpy as np
import sympy as sp

class ProblemParser:

    def __init__(self, json_data) -> None:
        #self.ne_parser = parser_numexpr() #parse function 
        self.constants = self.constants_parser(json_data["Constants"])
        self.varibles,self.var_names = self.varibles_parser(json_data["Varibles"])
        self.objectives = self.objectives_parser(json_data["Objectives"])

    def json_to_sympy(self,json_expr):
        if isinstance(json_expr, str):
            # Handle variable symbols
            return sp.symbols(json_expr)
        elif isinstance(json_expr, int) or isinstance(json_expr, float):
            # Handle numeric constants
            return sp.Number(json_expr)
        elif isinstance(json_expr, list):
            # Handle function expressions
            if json_expr[0] == "Add":
                # Addition operation
                return sp.Add(*[self.json_to_sympy(sub_expr) for sub_expr in json_expr[1:]])
            elif json_expr[0] == "Multiply":
                # Multiplication operation
                return sp.Mul(*[self.json_to_sympy(sub_expr) for sub_expr in json_expr[1:]])
            elif json_expr[0] == "Sqrt":
                # Square root operation
                return sp.sqrt(self.json_to_sympy(json_expr[1]))
            elif json_expr[0] == "Divide":
                # Square root operation
                return self.json_to_sympy(json_expr[1])/self.json_to_sympy(json_expr[2])
        else:
            raise ValueError("Invalid JSON expression")

    def list2value(self,l,dict):
        # str_expr = self.ne_parser.parser(l)
        # f = sp.parse_expr(str_expr)
        f = self.json_to_sympy(l)
        print(f)
        value = f.evalf(subs=dict) 
        return value

    def constants_parser(self, constants_dict):
        if constants_dict is None: return None
        #parse constants

        # constants_dict = json_data["Constants"]
        c_dict = {}
        c_len = constants_dict["Length"]
        for i in range(c_len):
            k = "C"+str(i+1)
            d = constants_dict[k]
            name = d["ShortName"]
            value = d["Value"]
            if isinstance(value,list):
                value = self.list2value(value,c_dict)
            c_dict[name] = value
        print(c_dict)
        return c_dict
    

    def varibles_parser(self,varibles_dict):
        if varibles_dict is None: return None
        desdeo_vars = []
        var_names = []
        var_len = varibles_dict["Length"]
        for i in range(var_len):
            k = "Var"+str(i+1)
            d = varibles_dict[k]
            name = d["ShortName"]
            lower_bound = d["LowerBound"]
            if isinstance(lower_bound,(list,str)):
                lower_bound = self.list2value(lower_bound, self.constants)
            upper_bound = d["UpperBound"]
            if isinstance(upper_bound,(list,str)):
                upper_bound = self.list2value(upper_bound, self.constants)
            initial_value = d["InitialValue"]
            if initial_value is None: 
                initial_value = (lower_bound+upper_bound)/2
            x = Variable(name, 
                            initial_value,
                            lower_bound,
                            upper_bound)
            var_names.append(name)
            desdeo_vars.append(x)
        return desdeo_vars,var_names
    
    def objectives_parser(self, objectives_dict):
        if objectives_dict is None: return None
        desdeo_objs = []
        obj_len = objectives_dict["Length"]
        for i in range(obj_len):
            obj_name = "Obj"+str(i+1)
            obj_dic = objectives_dict[obj_name]
            #handle the objective expressions
            # str_expr = self.ne_parser.parser(obj_dic["Func"])
            sympy_func = self.json_to_sympy(obj_dic["Func"])
            sympy_func = sympy_func.subs(self.constants)
            symbol_names = ','.join(self.var_names)
            # print(symbol_names)
            val = sp.symbols(symbol_names)
            lambda_func = sp.lambdify(val, sympy_func)
            desdeo_func = lambda x : lambda_func(*[x[:,i] for i in range(len(self.var_names))])

            desdeo_obj = ScalarObjective(obj_dic["ShortName"],
                                desdeo_func)
            desdeo_objs.append(desdeo_obj)

        return desdeo_objs
    def get_desdeo_problem(self):
        problem = ScalarMOProblem(objectives=self.objectives,
                                variables = self.varibles,
                                constraints=None)
        return problem

    def json2moproblem(self, json_data):
        #parsing the variables into desdeo variable.
        desdeo_vars = []
        var_names = []
        desdeo_objs = []
        desdeo_cons = []
        ne_parser = parser_numexpr() #parse function 


        


        #parse variables
        variables_dict = json_data["Varibles"]
        if variables_dict is not None:
            var_len = variables_dict["Length"]
            for i in range(var_len):
                var_name = "Var"+str(i+1)
                var_dic = variables_dict[var_name]
                var_names.append(var_dic["ShortName"])
                x = Variable(var_dic["ShortName"], 
                            var_dic["InitialValue"], 
                            var_dic["LowerBound"],
                            var_dic["UpperBound"])
                desdeo_vars.append(x)

        objectives_dict = json_data["Objectives"]
        if objectives_dict is not None:
            obj_len = objectives_dict["Length"]
            for j in range(obj_len):
                obj_name = "Obj"+str(j+1)
                obj_dic = objectives_dict[obj_name]
                #handle the objective expressions
                str_expr = ne_parser.parser(obj_dic["Func"])
                sympy_func = sp.parse_expr(str_expr)
                symbol_names = ','.join(var_names)
                val = sp.symbols(symbol_names)
                for jj in range(len(var_names)):
                    sympy_func = sympy_func.subs(var_names[jj],val[jj])
                temp = sp.lambdify(val, sympy_func,modules='numpy')
                
                print(desdeo_expr)
                desdeo_obj = ScalarObjective(obj_dic["ShortName"],
                                    desdeo_expr)
                desdeo_objs.append(desdeo_obj)

        constrainst_dict = json_data["Constraints"]
        if constrainst_dict is not None:
            con_len = constrainst_dict["Length"]
            for k in range(con_len):
                con_name = "Con"+str(k+1)
                con_dic = constrainst_dict[con_name]
                #handle the objective expressions
                str_expr = ne_parser.parser(con_dic["Func"])
                print(str_expr)
                name_index = 0
                for name in var_names:
                    str_expr = str_expr.replace(name,str("x[:,{}]".format(name_index)))
                    name_index+=1
                desdeo_expr = str2constraints(str_expr)
                desdeo_con = ScalarConstraint(con_dic["ShortName"],var_len,obj_len,
                                    desdeo_expr)
                desdeo_cons.append(desdeo_con)

        # Args: name, n of variables, n of objectives, callable
        problem = ScalarMOProblem(objectives=desdeo_objs,
                                variables = desdeo_vars,
                                constraints= desdeo_cons)
        return problem
    
#be careful with this function, eval and desdeo lambda should be TOGETHER OUTSIDE the local life cycle .
def str2objectives(str_expr):
    lambda_str = "lambda x:{}".format(str_expr)
    desdeo_expr = eval(lambda_str)
    return desdeo_expr

def str2constraints(str_expr):
    lambda_str = "lambda x,_:{}".format(str_expr)
    desdeo_expr = eval(lambda_str)
    return desdeo_expr


    
#convert the json dictionary into desdeo standard problems
def json2moproblem(json_data):
    #parsing the variables into desdeo variable.
    desdeo_vars = []
    var_names = []
    desdeo_objs = []
    desdeo_cons = []
    ne_parser = parser_numexpr() #parse function 
    constants = {}
    constants_dict = json_data["Constants"]
    if constants_dict is not None:
        c_len = constants_dict["Length"]
        for i in range(c_len):
            c_name = "C"+str(i+1)
            c_dic = constants_dict[c_name]
            value = c_dic["Value"]
            if isinstance(value, list):
                str_expr = ne_parser.parser(value)
                # value = eval(str_expr)
            constants[c_name] = value
    variables_dict = json_data["Varibles"]
    if variables_dict is not None:
        var_len = variables_dict["Length"]
        for i in range(var_len):
            var_name = "Var"+str(i+1)
            var_dic = variables_dict[var_name]
            var_names.append(var_dic["ShortName"])
            x = Variable(var_dic["ShortName"], 
                        var_dic["InitialValue"], 
                        var_dic["LowerBound"],
                        var_dic["UpperBound"])
            desdeo_vars.append(x)
    objectives_dict = json_data["Objectives"]
    if objectives_dict is not None:
        obj_len = objectives_dict["Length"]
        for j in range(obj_len):
            obj_name = "Obj"+str(j+1)
            obj_dic = objectives_dict[obj_name]
            #handle the objective expressions
            str_expr = ne_parser.parser(obj_dic["Func"])
            print(str_expr)
            name_index = 0
            for name in var_names:
                str_expr = str_expr.replace(name,str("x[:,{}]".format(name_index)))
                name_index+=1
            desdeo_expr = str2objectives(str_expr)
            desdeo_obj = ScalarObjective(obj_dic["ShortName"],
                                desdeo_expr)
            desdeo_objs.append(desdeo_obj)

    constrainst_dict = json_data["Constraints"]
    if constrainst_dict is not None:
        con_len = constrainst_dict["Length"]
        for k in range(con_len):
            con_name = "Con"+str(k+1)
            con_dic = constrainst_dict[con_name]
            #handle the objective expressions
            str_expr = ne_parser.parser(con_dic["Func"])
            print(str_expr)
            name_index = 0
            for name in var_names:
                str_expr = str_expr.replace(name,str("x[:,{}]".format(name_index)))
                name_index+=1
            desdeo_expr = str2constraints(str_expr)
            desdeo_con = ScalarConstraint(con_dic["ShortName"],var_len,obj_len,
                                desdeo_expr)
            desdeo_cons.append(desdeo_con)

    # Args: name, n of variables, n of objectives, callable
    problem = ScalarMOProblem(objectives=desdeo_objs,
                            variables = desdeo_vars,
                            constraints= desdeo_cons)
    return problem

#Testing 
import json
# Opening JSON file
f = open('math_json_parser/RE-21.json')  
# returns JSON object as 
# a dictionary

data = json.load(f)
pp = ProblemParser(data)
# test_constants = pp.constant_parser(data["Constants"])
problem = pp.get_desdeo_problem()
# print(test_constants)
# problem = pp.json2moproblem(data)
print("N of objectives:", problem.n_of_objectives)
print("N of variables:", problem.n_of_variables)
print("N of constraints:", problem.n_of_constraints)

res1 = problem.evaluate(np.array([2, 4, 6,8]))
res2 = problem.evaluate(np.array([6, 6,6,6]))
res3 = problem.evaluate(np.array([[6, 3,7,4], [4,3,8,6], [7,4,5,6]]))

print("Single feasible decision variables:", res1.objectives, "with constraint values", res1.constraints)
print("Single non-feasible decision variables:", res2.objectives, "with constraint values", res2.constraints)
print("Multiple decision variables:", res3.objectives, "with constraint values", res3.constraints)