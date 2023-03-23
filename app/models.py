from pydantic import BaseModel


class FixRequest(BaseModel):
    dimacs: str


class LinkRequest(BaseModel):
    firstDimacs: str
    secondDimacs: str


class SolveRequest(BaseModel):
    solver: str
    dimacs: str


class NextRequest(BaseModel):
    solver: str
    formula: str
