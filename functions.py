from datetime import datetime

def geraID():
    datahora = datetime.now()
    id = datahora.strftime('%d%m%H%M%S%f')
    id = 1 + int(id)
    return id

def validPerson(data,param_update):

    response = {
        "status":False,
        "msg":""
    }

    nome = data.get('nome')
    idade = data.get('idade')

    if param_update != True:
        if nome == "":
            response['msg'] = 'the nome field cannot be empty'
            return response
    

    if len(nome) > 35:
        response['msg'] = 'the name field cannot be longer than 35 characters'
        return response
    
    if param_update != True:
        if idade == "":
            response['msg'] = 'the idade field cannot be empty'
            return response
    
    if idade <= 0:
        response['msg'] = 'the idade field cannot be less than or equal to 0'
        return response
    
    response['status'] = True
    return response


