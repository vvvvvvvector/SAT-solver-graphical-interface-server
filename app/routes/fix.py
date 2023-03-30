import schemas
import utils

from fastapi import APIRouter

fixroute = APIRouter()


@fixroute.post('/fix')
def fix(request: schemas.FixRequest):
    file_by_lines = request.dimacs.split('\n')

    variables = set()
    clauses_amount = 0

    clauses = ""

    for line in file_by_lines[0:]:
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
