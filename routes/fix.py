import schemas
import utils

from fastapi import APIRouter

fixroute = APIRouter()


@fixroute.post('/fix')
def fix(request: schemas.FixRequest):
    file_by_lines = request.dimacs.split('\n')

    # removing empty lines if there are any
    file_by_lines = list(filter(None, file_by_lines))

    variables = set()
    clauses_amount = 0

    clauses = ""

    for line in file_by_lines:
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

    variables = sorted(variables)

    return {
        "fixed": f"p cnf {variables[len(variables) - 1]} {clauses_amount}\n" + clauses[:-1]
    }


@fixroute.post('/remove-duplicates')
def remove(request: schemas.FixRequest):
    file_by_lines = request.dimacs.split('\n')

    # removing empty lines if there are any
    file_by_lines = list(filter(None, file_by_lines))

    formula_params = list(filter(None, file_by_lines[0].split(' ')))

    clauses_int = []

    clauses = []

    for line in file_by_lines[1:]:
        clauses.append(" ".join(list(filter(None, line.split(' ')))))

    for line in file_by_lines[1:]:
        clauses_int.append(
            list(map(int, filter(lambda x: x != '' and x != '0', line.split(' ')))))

    for clause in clauses_int:
        clause.sort()

    for i in range(len(clauses_int)):
        clauses[i] = " ".join(list(map(str, clauses_int[i]))) + " 0"

    no_duplicates = utils.remove_duplicates(clauses)

    return {
        "fixed": f"p cnf {formula_params[2]} {len(no_duplicates)}\n" + "\n".join(no_duplicates)
    }
