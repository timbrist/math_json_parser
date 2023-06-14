from desdeo_problem import Variable, ScalarObjective, ScalarConstraint, ScalarMOProblem
from parser_numexpr import parser_numexpr
import numpy as np
import sympy as sp

class ProblemParser:
    
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
            if json_expr[0] == "Substract":
                # Addition operation
                result = self.json_to_sympy(json_expr[1]) 
                for sub_expr in json_expr[2:]:
                    result = result - self.json_to_sympy(sub_expr)
                return result
            elif json_expr[0] == "Multiply":
                # Multiplication operation
                return sp.Mul(*[self.json_to_sympy(sub_expr) for sub_expr in json_expr[1:]])
            elif json_expr[0] == "Sqrt":
                # Square root operation
                return sp.sqrt(self.json_to_sympy(json_expr[1]))
            elif json_expr[0] == "Squre":
                # Square root operation
                return self.json_to_sympy(json_expr[1])**2
            elif json_expr[0] == "Divide":
                # Square root operation
                # return self.json_to_sympy(json_expr[1])/self.json_to_sympy(json_expr[2])
                result = self.json_to_sympy(json_expr[1]) 
                for sub_expr in json_expr[2:]:
                    result = result / self.json_to_sympy(sub_expr)
                return result
        else:
            raise ValueError("Invalid JSON expression")

    def list_to_value(self,l,dict):
        f = self.json_to_sympy(l)
        value = f.evalf(subs=dict) 
        return value


    def function_parser(self, function_dict, constants, var_names, isConstraint=False):
        sympy_func = self.json_to_sympy(function_dict)
        print(sympy_func)
        if constants is not None:
            sympy_func = sympy_func.subs(constants)
        symbol_names = ','.join(var_names)
        val = sp.symbols(symbol_names)
        # lambda_func = sp.Lambda(val, sympy_func)
        lambda_func = sp.lambdify(val, sympy_func)
        if isConstraint:
            desdeo_func = lambda x,_ : lambda_func(*[x[:,i] for i in range(len(var_names))])
        else:
            desdeo_func = lambda x : lambda_func(*[x[:,i] for i in range(len(var_names))])
        return desdeo_func

    def constants_parser(self, constants_dict):
        if constants_dict is None: return None
        c_dict = {}
        c_len = constants_dict["Length"]
        for i in range(c_len):
            k = "C"+str(i+1)
            d = constants_dict[k]
            name = d["ShortName"]
            value = d["Value"]
            if isinstance(value,list):
                value = self.list_to_value(value,c_dict)
            c_dict[name] = value
        # print(c_dict)
        return c_dict
    

    def varibles_parser(self, varibles_dict, constants):

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
                lower_bound = self.list_to_value(lower_bound, constants)
            upper_bound = d["UpperBound"]
            if isinstance(upper_bound,(list,str)):
                upper_bound = self.list_to_value(upper_bound, constants)
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
    
    def objectives_parser(self, objectives_dict,constants, var_name):
        if objectives_dict is None: return None
        desdeo_objs = []
        obj_len = objectives_dict["Length"]
        for i in range(obj_len):
            obj_name = "Obj"+str(i+1)
            obj_dic = objectives_dict[obj_name]

            desdeo_func = self.function_parser(obj_dic["Func"],constants, var_name,False)
            # test = np.array([2, 4])
            # print(desdeo_func(test))
            desdeo_obj = ScalarObjective(obj_dic["ShortName"],
                                desdeo_func)
            desdeo_objs.append(desdeo_obj)        
        return desdeo_objs
    
    def constraints_parser(self, constraints_dict,constants,var_name,n_objective_funs):
        if constraints_dict is None: return None
        desdeo_cons = []
        con_len = constraints_dict["Length"]
        for i in range(con_len):
            con_name = "Con"+str(i+1)
            con_dic = constraints_dict[con_name]
            desdeo_func = self.function_parser(con_dic["Func"],constants, var_name,isConstraint=True)
            
            desdeo_con = ScalarConstraint(con_dic["ShortName"],len(var_name),n_objective_funs,
                                desdeo_func)
            desdeo_cons.append(desdeo_con)        
        return desdeo_cons

    def json_to_desdeo(self, json_data):

        constants = self.constants_parser(json_data["Constants"])
        print(constants)
        varibles, var_names = self.varibles_parser(json_data["Varibles"], constants)
        print(varibles, var_names )
        objectives = self.objectives_parser(json_data["Objectives"], constants, var_names)
        print(objectives)
        constraints = self.constraints_parser(json_data["Constraints"],constants, var_names,len(objectives))

        problem = ScalarMOProblem(objectives=objectives,
                                variables = varibles,
                                constraints=constraints)
        return problem

# #Testing 
import json


# # Opening JSON file

# f = open('math_json_parser/RE-21.json')  

# data = json.load(f)
# pp = ProblemParser()
# problem = pp.json_to_desdeo(data)

# print("N of objectives:", problem.n_of_objectives)
# print("N of variables:", problem.n_of_variables)
# print("N of constraints:", problem.n_of_constraints)

# res1 = problem.evaluate(np.array([2, 4, 6,8]))
# res2 = problem.evaluate(np.array([6, 6,6,6]))
# res3 = problem.evaluate(np.array([[6, 3,7,4], [4,3,8,6], [7,4,5,6]]))

# print("Single feasible decision variables:", res1.objectives, "with constraint values", res1.constraints)
# print("Single non-feasible decision variables:", res2.objectives, "with constraint values", res2.constraints)
# print("Multiple decision variables:", res3.objectives, "with constraint values", res3.constraints)




f = open('math_json_parser/moo_json_format.json')  
data = json.load(f)
pp = ProblemParser()
problem = pp.json_to_desdeo(data)

print("N of objectives:", problem.n_of_objectives)
print("N of variables:", problem.n_of_variables)
print("N of constraints:", problem.n_of_constraints)

res1 = problem.evaluate(np.array([2, 4]))
res2 = problem.evaluate(np.array([6, 6]))
res3 = problem.evaluate(np.array([[6, 3], [4,3], [7,4]]))

print("Single feasible decision variables:", res1.objectives, "with constraint values", res1.constraints)
print("Single non-feasible decision variables:", res2.objectives, "with constraint values", res2.constraints)
print("Multiple decision variables:", res3.objectives, "with constraint values", res3.constraints)