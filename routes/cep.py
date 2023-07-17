from fastapi import APIRouter,HTTPException
import requests
import xmltodict
from requests.exceptions import ConnectionError
from fastapi.responses import JSONResponse
from database import Database
from model import Cep
import os
from dotenv import load_dotenv



person_route = APIRouter(prefix='/api')

load_dotenv()
url = os.getenv('DATABASE_URL')
db = Database(url)

cep_route = APIRouter(prefix='/api')

@cep_route.get("/cep/{cep_api:str}", response_model=Cep)
async def get_cep(cep_api:str):
    
    cep_api = cep_api.replace("-","")
    response_json = {"sucesso":False}
    cache = await get_person_by_cep(cep_api)

    if cache != False:
       response_json['sucesso'] = True
       response_json['endereco'] = cache
       return JSONResponse(response_json,status_code=200)
    else:
        
        url_cep = f'https://viacep.com.br/ws/{cep_api}/xml/'
        try:
            r = requests.get(url_cep, timeout=5)
        except ConnectionError:
            return JSONResponse(response_json,status_code=502)

        status = r.status_code

        if status == 200:

            response = r.content
            xml_parsed = xmltodict.parse(response)
            xml_cep = xml_parsed.get('xmlcep','Not Found')
            
            if xml_cep.get('erro'):
                response_json['error'] = 'Cep not found'
                return JSONResponse(response_json,status_code=404)
            
           
            logradouro = xml_cep.get('logradouro','Not Found')
            complemento = xml_cep.get('complemento','Not Found')
            bairro = xml_cep.get('bairro','Not Found')
            cidade = xml_cep.get('localidade','Not Found')
            uf = xml_cep.get('uf','Not Found')
            response_json['sucesso'] = True

            endereco = {
                "cep":cep_api,
                "logradouro":logradouro,
                "complemento":complemento,
                "bairro":bairro,
                "cidade":cidade,
                "uf":uf
            }
            response_json['endereco'] = endereco
            await post_cep(endereco)
            print("create")
            

        elif status == 400:
            response_json['error'] = 'Cep not found'
            status = 404
        else:
            response_json['error'] = 'Unknown error'
    
        return JSONResponse(response_json,status_code=200)

async def get_person_by_cep(cep):
    response = await db.fetch_one_cep(cep)
    if response:
        del response['_id']
        return response
    else:
        return False
    
async def post_cep(cep:Cep):
    response = await db.create_cep(cep)
    if response:
        return response
    raise HTTPException(400, "Bad Request")
    