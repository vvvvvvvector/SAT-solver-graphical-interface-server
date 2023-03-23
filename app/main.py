from pysat.solvers import Solver

import utils
from models import SolveRequest, NextRequest, LinkRequest, FixRequest

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware

import json

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["POST"],
    allow_headers=["*"]
)


@app.get('/')
def root():
    return {'message': 'backend is running...'}


@app.post('/fix')
def fix(requst: FixRequest):
    file_by_lines = requst.dimacs.split('\n')

    variables = set()
    clauses_amount = 0

    clauses = ""

    for line in file_by_lines[1:]:
        clause = list(filter(None, line.split(' ')))

        try:
            for variable in utils.string_to_int(clause):
                variables.add(abs(variable))

            clause_string = " ".join(clause)

            if clause_string[len(clause_string) - 1] != '0':
                clause_string += ' 0'

            clauses += clause_string + "\n"

            clauses_amount += 1

        except:
            print(f"Error while parsing line: {line}")

    return {
        "fixed": f"p cnf {len(variables)} {clauses_amount}\n" + clauses[:-1]
    }


@app.post('/link')
def link(request: LinkRequest):
    print(request.firstDimacs)

    print(request.secondDimacs)

    return {
        "success": True
    }


@ app.post('/solve')
def solve(request: SolveRequest):
    solver = Solver(request.solver)  # creating a solver

    # dividing the cnf file into lines
    file_by_lines = request.dimacs.split('\n')

    # getting parameters of the formula (variables_amount, clauses_amount)
    params = list(filter(None, file_by_lines[0].split(' ')))

    clauses = []

    variables_amount = int(params[2])
    clauses_amount = int(params[3])

    # checking if the number of clauses is correct
    if clauses_amount != len(file_by_lines) - 1:
        raise HTTPException(
            status_code=418, detail=f"Wrong number of clauses!\nIn formula definition: {clauses_amount}\nIn dimacs: {len(file_by_lines) - 1}")

    for i in range(clauses_amount):
        clause = utils.string_to_int(
            list(filter(None, file_by_lines[i + 1].split(' '))))

        # checking if the clause is correct
        for variable in clause:
            if abs(variable) > variables_amount:
                raise HTTPException(
                    status_code=419, detail=f"Wrong variable value!\nError in line: {i + 2}")

        clauses.append({"id": i, "variables": clause})

        solver.add_clause(clause)

    satisfiable = solver.solve()

    first_solution = solver.get_model()

    solver.delete()

    if satisfiable != False:
        clauses.append({"id": clauses_amount,
                       "variables": list(map(lambda x: x * -1, first_solution))})

        return {
            "satisfiable": satisfiable,
            "clauses": clauses,
            "first_solution": first_solution
        }
    else:
        return {
            "satisfiable": False,
            "clauses": clauses,
            "first_solution": []
        }


@ app.post('/next-solution')
def next(request: NextRequest):
    solver = Solver(request.solver)  # creating a solver

    parsed_formula = json.loads(request.formula)

    for clause in parsed_formula:
        solver.add_clause(clause["variables"])

    satisfiable = solver.solve()

    next_solution = solver.get_model()

    solver.delete()

    if satisfiable != False:
        parsed_formula.append({"id": parsed_formula[len(parsed_formula) - 1]["id"] + 1, "variables": list(
            map(lambda x: x * -1, next_solution))})

        return {
            "satisfiable": satisfiable,
            "clauses": parsed_formula,
            "next_solution": next_solution
        }
    else:
        return {
            "satisfiable": False
        }
