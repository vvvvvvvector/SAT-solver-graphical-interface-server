from pysat.solvers import Solver

import schemas

import json

from fastapi import APIRouter

nextroute = APIRouter()


@nextroute.post('/next-solution')
def next(request: schemas.NextRequest):
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
