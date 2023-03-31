from pysat.solvers import Solver

import schemas
import utils

from fastapi import APIRouter, HTTPException

solveroute = APIRouter()


@solveroute.post('/solve')
def solve(request: schemas.SolveRequest):
    solver = Solver(request.solver)  # creating a solver

    # dividing the cnf file into lines
    file_by_lines = request.dimacs.split('\n')

    # removing empty lines if there are any
    file_by_lines = list(filter(None, file_by_lines))

    # getting parameters of the formula (variables_amount, clauses_amount)

    if file_by_lines[0].startswith("p cnf"):
        params = list(filter(None, file_by_lines[0].split(' ')))
    else:
        raise HTTPException(
            status_code=420, detail="There is no formula definition!")

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
