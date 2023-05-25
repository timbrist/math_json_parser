from desdeo_problem import Variable, ScalarObjective, ScalarConstraint, ScalarMOProblem
import json

# Opening JSON file
f = open('math_json_parser/moo_json_format.json')
  
# returns JSON object as 
# a dictionary
data = json.load(f)

print(type(data))

from parser_numexpr import parser_numexpr
test = parser_numexpr()
testlist = ["Substract",["Squre","x1"],"x2"]
str_expr = test.parser(testlist)
expr = lambda x1,x2: eval(str_expr)
print(expr(2,3))
#TODO: initial value, lower bound and upper will be 1. none, 2. a function, 3. number
# def json2moproblem(json_data:dict)-> ScalarMOProblem:
def json2moproblem(json_data):
    
    variables_dict = json_data["Varibles"]
    X = []
    for k in variables_dict:
        var_dic = variables_dict[k]
        if isinstance(var_dic,dict):
            x = Variable(var_dic["ShortName"], 
                         var_dic["InitialValue"], 
                         var_dic["LowerBound"],
                         var_dic["UpperBound"])
            X.append(x)
    objectives_dict = json_data["Objectives"]
    
    # for k in objectives_dict:
    #     obj_dic = objectives_dict[k]
    #     if isinstance(obj_dic,dict):
    #         obj = ScalarObjective()

    obj1 = ScalarObjective("f_1", lambda x: expr(x[:,0],x[:,1]))

    obj1 = ScalarObjective("f_1", lambda x: x[:,0]**2 - x[:,1])
    obj2 = ScalarObjective("f_2", lambda x: x[:,1]**2 - 3*x[:,0])
    OBJS = [obj1,obj2]
    cons1 = ScalarConstraint("c_1", 2, 2, lambda x, _: 10 - (x[:,0] + x[:,1]))
    CONS = [cons1]
    # Args: list of objevtives, variables and constraints
    problem = ScalarMOProblem(objectives=OBJS,
                              variables = X,
                              constraints= CONS)
    return problem


problem = json2moproblem(data)

import numpy as np

print("N of objectives:", problem.n_of_objectives)
print("N of variables:", problem.n_of_variables)
print("N of constraints:", problem.n_of_constraints)

res1 = problem.evaluate(np.array([2, 4]))
res2 = problem.evaluate(np.array([6, 6]))
res3 = problem.evaluate(np.array([[6, 3], [4,3], [7,4]]))

print("Single feasible decision variables:", res1.objectives, "with constraint values", res1.constraints)
print("Single non-feasible decision variables:", res2.objectives, "with constraint values", res2.constraints)
print("Multiple decision variables:", res3.objectives, "with constraint values", res3.constraints)