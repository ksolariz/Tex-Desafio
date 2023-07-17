from model import Person
from motor.motor_asyncio import AsyncIOMotorClient
class Database:

    def __init__(self,url):
        self.url = url
        self.client = AsyncIOMotorClient(self.url)
        self.database_person = self.client.PersonList
        self.collection_person = self.database_person.person

        self.database_cep = self.client.CepList
        self.collection_cep = self.database_cep.cep

    #Person
    async def fetch_one_person(self,id):
        document = await self.collection_person.find_one({"id":id})
        return document
    
    async def fetch_all_persons(self):
        persons = []
        cursor = self.collection_person.find({})
        async for document in cursor:
            persons.append(Person(**document))
        return persons
    
    async def create_person(self,person):
        document = person
        await self.collection_person.insert_one(document)
        return document
    
    async def update_person(self,id,data):
        nome = data.get('nome')
        idade = data.get('idade')

        document = await self.collection_person.find_one({"id":id})
        if nome == "":
            nome = document['nome']
        if idade == "":
            idade = document['idade']


        await self.collection_person.update_one({"id":id},{"$set":{
            "nome":nome,
            "idade":idade
        }})
        document = await self.collection_person.find_one({"id":id})
        return document
    
    async def remove_person(self,id):
        await self.collection_person.delete_one({"id":id})
        return True
    
    #Cep
    async def fetch_one_cep(self,cep):
        document = await self.collection_cep.find_one({"cep":cep})
        return document
    
    async def create_cep(self,endereco):
        document = endereco
        await self.collection_cep.insert_one(document)
        del document['_id']
        return document