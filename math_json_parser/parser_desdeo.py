from desdeo_problem import Variable, ScalarObjective, ScalarConstraint, ScalarMOProblem
from parser_numexpr import parser_numexpr
import numpy as np

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

    variables_dict = json_data["Varibles"]
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
f = open('math_json_parser/moo_json_format.json')  
# returns JSON object as 
# a dictionary
data = json.load(f)
problem = json2moproblem(data)
print("N of objectives:", problem.n_of_objectives)
print("N of variables:", problem.n_of_variables)
print("N of constraints:", problem.n_of_constraints)

res1 = problem.evaluate(np.array([2, 4]))
res2 = problem.evaluate(np.array([6, 6]))
res3 = problem.evaluate(np.array([[6, 3], [4,3], [7,4]]))

print("Single feasible decision variables:", res1.objectives, "with constraint values", res1.constraints)
print("Single non-feasible decision variables:", res2.objectives, "with constraint values", res2.constraints)
print("Multiple decision variables:", res3.objectives, "with constraint values", res3.constraints)