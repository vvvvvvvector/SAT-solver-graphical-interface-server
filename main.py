from fastapi import FastAPI
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware

from pysat.solvers import Solver

app = FastAPI()

server_state = {
    "solver": "cd",
    "clauses_n": 0,
    "clauses": []
}

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)


def string_to_int(string_arr):
    int_arr = []
    for i in range(len(string_arr) - 1):
        int_arr.append(int(string_arr[i]))
    return int_arr


class Request(BaseModel):
    solver: str
    formula: str


@app.get('/')
def root():
    return {
        "message": "Hello from FastAPI.",
        "selected_solver": server_state["solver"],
        "clauses_n": server_state["clauses_n"],
        "clauses": server_state["clauses"]
    }


@app.get('/find-next-solution')
def solve_one_more():
    solver = Solver(server_state["solver"])

    for i in range(server_state["clauses_n"]):
        clause = server_state["clauses"][i]["variables"]
        solver.add_clause(clause)

    satisiable = solver.solve()

    model = solver.get_model()

    if model != None:
        server_state["clauses"].append(
            {"id": server_state["clauses_n"], "variables": list(map(lambda x: x * -1, model))})
        server_state["clauses_n"] += 1

    solver.delete()

    return {
        "clause": (server_state["clauses"][server_state["clauses_n"] - 1] if model != None else []),
        "satisfiable": satisiable
    }


@app.post('/solve-my-problem')
def solve_my_problem(request: Request):
    server_state["solver"] = request.solver

    solver = Solver(server_state["solver"])

    server_state["clauses_n"] = 0
    server_state["clauses"] = []

    string_lines = request.formula.split('\n')

    params = string_lines[0].split(' ')

    server_state["clauses_n"] = int(params[3])

    for i in range(int(params[3])):
        clause = string_to_int(string_lines[i + 1].split(' '))
        server_state["clauses"].append({"id": i, "variables": clause})
        solver.add_clause(clause)

    satisfiable = solver.solve()

    model = solver.get_model()

    if model != None:
        server_state["clauses"].append(
            {"id": server_state["clauses_n"], "variables": list(map(lambda x: x * -1, model))})
        server_state["clauses_n"] += 1

    solver.delete()

    return {
        "formula": request.formula,
        "clauses": server_state["clauses"][:-1],
        "model": server_state["clauses"][server_state["clauses_n"] - 1],
        "satisfiable": satisfiable
    }
