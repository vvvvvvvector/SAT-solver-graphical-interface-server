from fastapi import FastAPI
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware

from pysat.solvers import Solver


def string_to_int(string_arr):
    int_arr = []
    for i in range(len(string_arr) - 1):
        int_arr.append(int(string_arr[i]))
    return int_arr


class Item(BaseModel):
    formula: str


app = FastAPI()


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)

formula = {
    "length": 0,
    "clauses": []
}

solver_name = 'mgh'


@app.get('/')
async def root():
    return {
        "message": "Hello from server!",
        "length": formula["length"],
        "store": formula["clauses"]
    }


@app.get('/solve-one-more')
async def solve_one_more():
    solver = Solver(name=solver_name)

    for i in range(formula["length"]):
        clause = formula["clauses"][i]
        solver.add_clause(clause)

    satisiable = solver.solve()

    model = solver.get_model()

    if model != None:
        formula["clauses"].append(list(map(lambda x: x * -1, model)))
        formula["length"] += 1

    solver.delete()

    return {
        "model": model,
        "satisfiable": satisiable
    }


@app.post('/solve-my-problem')
async def solve_my_problem(item: Item):
    solver = Solver(name=solver_name)

    formula["length"] = 0
    formula["clauses"] = []

    string_lines = item.formula.split('\n')

    params = string_lines[0].split(' ')

    formula["length"] = int(params[3])

    for i in range(int(params[3])):
        clause = string_to_int(string_lines[i + 1].split(' '))
        formula["clauses"].append(clause)
        solver.add_clause(clause)

    satisiable = solver.solve()

    model = solver.get_model()

    if model != None:
        formula["clauses"].append(list(map(lambda x: x * -1, model)))
        formula["length"] += 1

    solver.delete()

    return {
        "formula": item.formula,
        "result": {
            "model": model,
            "satisfiable": satisiable
        }
    }
