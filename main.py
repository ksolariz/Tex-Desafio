from fastapi import FastAPI, APIRouter

from routes.cep import cep_route
from routes.person import person_route

app = FastAPI()
router = APIRouter()

@app.get("/")
async def read_root():
    return {"Hello": "World"}

app.include_router(cep_route)
app.include_router(person_route)

    
