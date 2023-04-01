import schemas

from fastapi import APIRouter, HTTPException

import utils

linkroute = APIRouter()


@linkroute.post('/link')
def link(request: schemas.LinkRequest):
    first_by_lines = request.firstDimacs.split('\n')
    second_by_lines = request.secondDimacs.split('\n')

    if not first_by_lines[0].startswith("p cnf"):
        raise HTTPException(
            status_code=422, detail="There is no formula definition in the first formula!"
        )

    if not second_by_lines[0].startswith("p cnf"):
        raise HTTPException(
            status_code=423, detail="There is no formula definition in the second formula!"
        )

    # removing empty lines if there are any
    first_by_lines = list(filter(None, first_by_lines))
    second_by_lines = list(filter(None, second_by_lines))

    print(first_by_lines)
    print(second_by_lines)

    if utils.compare_formulas(first_by_lines, second_by_lines):
        raise HTTPException(
            status_code=421, detail="Formulas are the same!"
        )

    return {
        "success": True
    }
