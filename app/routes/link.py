import schemas

from fastapi import APIRouter

linkroute = APIRouter()


@linkroute.post('/link')
def link(request: schemas.LinkRequest):
    print(request.firstDimacs)

    print(request.secondDimacs)

    return {
        "success": True
    }
