from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from routes.solve import solveroute
from routes.fix import fixroute
from routes.link import linkroute
from routes.next import nextroute

app = FastAPI()


@app.get('/')
def root():
    return {'message': 'backend is running...'}


app.include_router(solveroute)

app.include_router(nextroute)

app.include_router(fixroute)

app.include_router(linkroute)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["POST"],
    allow_headers=["*"]
)
