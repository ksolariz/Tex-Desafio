from pydantic import BaseModel,Field

class Cep(BaseModel):
    cep:str
    logradouro:str
    complemento:str
    bairro:str
    cidade:str
    uf:str

class Person(BaseModel):
    id:int = Field(hidden_from_schema=True)
    nome:str
    idade:int

class PersonRequest(BaseModel):
    nome:str
    idade:int

