import schemas

import re

from fastapi import APIRouter, HTTPException

import utils

linkroute = APIRouter()


@linkroute.post('/link')
def link(request: schemas.LinkRequest):
    first_by_lines = request.firstDimacs.split('\n')
    second_by_lines = request.secondDimacs.split('\n')

    if re.search(r"^p\s+cnf\s+[1-9][0-9]*\s+[1-9][0-9]*\s*$", first_by_lines[0]) == None:
        raise HTTPException(
            status_code=422, detail="There is no formula definition in the first formula!"
        )

    if re.search(r"^p\s+cnf\s+[1-9][0-9]*\s+[1-9][0-9]*\s*$", second_by_lines[0]) == None:
        raise HTTPException(
            status_code=423, detail="There is no formula definition in the second formula!"
        )

    # removing empty lines if there are any
    first_by_lines = list(filter(None, first_by_lines))
    second_by_lines = list(filter(None, second_by_lines))

    if utils.compare_formulas(first_by_lines, second_by_lines):
        raise HTTPException(
            status_code=421, detail="Formulas are the same!"
        )

    clauses = []

    for line in first_by_lines[1:]:
        clauses.append(" ".join(list(filter(None, line.split(' ')))))

    for line in second_by_lines[1:]:
        clauses.append(" ".join(list(filter(None, line.split(' ')))))

    # clauses list without duplicates
    no_duplicates = utils.remove_duplicates(clauses)

    variables = set()

    for line in no_duplicates:
        clause = list(filter(None, line.split(' ')))

        try:
            for variable in utils.string_to_int(clause):
                variables.add(abs(variable))

        except:
            print(f"Error while parsing line: {line}")

    return {
        "result": f"p cnf {len(variables)} {len(no_duplicates)}\n" + "\n".join(no_duplicates)
    }
