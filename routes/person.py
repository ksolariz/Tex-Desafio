from fastapi import APIRouter, HTTPException
from fastapi.responses import JSONResponse
from model import Person,PersonRequest
from database import Database
import os
from dotenv import load_dotenv
from functions import geraID, validPerson


person_route = APIRouter(prefix='/api')

load_dotenv()
url = os.getenv('DATABASE_URL')
db = Database(url)

@person_route.get("/person/")
async def get_all_person():
    response = await db.fetch_all_persons()
    return response

@person_route.get("/person/{id}", response_model=Person)
async def get_person_by_id(id:int):
    response = await db.fetch_one_person(id)
    if response:
        return response
    raise HTTPException(404,f"there is no person with this ID {id}")

@person_route.post("/person/", response_model=Person)
async def post_person(person:PersonRequest):
    data = person.dict()
    validation = validPerson(data,False)

    if validation['status'] == False:
        msg = {
            "message":validation['msg']
        }
        return JSONResponse(msg,400)
    else:
        data['id'] = geraID()
        response = await db.create_person(data)
        if response:
            return response
        raise HTTPException(400, "Bad Request")


@person_route.put("/person/{id}", response_model=Person)
async def put_person(id:int,person:PersonRequest):
    data = person.dict()
    
    validation = validPerson(data,True)

    if validation['status'] == False:
        msg = {
            "message":validation['msg']
        }
        return JSONResponse(msg,400)
    else:
        response = await db.update_person(id,data)
    if response:
        return response
    raise HTTPException(404,f"there is no person with this ID {id}")

@person_route.delete("/person/{id}")
async def delete_person(id:int):
    response = await db.fetch_one_person(id)
    if response:
        await db.remove_person(id)
        return "Succesfully deleted"
    raise HTTPException(404,f"there is no person with this ID {id}")




