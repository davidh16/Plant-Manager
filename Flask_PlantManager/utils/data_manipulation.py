
def retrieved_data_to_json(retrieved_data):
    # funkcija koja pretvara povečene podatke iz baze podataka u json format

    json = {}
    for item in retrieved_data:
        temp = {'username' : item[1],
                'name' : item[2],
                'surname' : item[3],
                'job' : item[4],
                'access_level' : item[5],
                'date_of_employment' : item[6],
                'broj_telefona' : item[7],
                'income' : item[8],
                'date_of_birth' : item[13]}
        json[item[0]] = temp
    return json

def partial_data_to_json(partial_data):
    json={}
    for item in partial_data:
        temp = {'username' : item[1],
                'name' : item[2],
                'surname' : item[3],
                'job' : item[4],
                'access_level' : item[5]}
        json[item[0]] = temp
    return json

def retrieved_items_to_json(retrieved_items):
    json = {}
    print(retrieved_items)
    for item in retrieved_items:
        temp = {'name': item[1],
                'quantity': item[2],
                'critical quantity': item[3],
                'brand': item[4],
                'supplier': item[5],
                'catalogue_number': item[6],
                'type': item[7],
                'model': item[8]}
        json[item[0]] = temp
    return json

def item_to_json(item):
    json={}
    temp = {'name': item[1],
            'quantity': item[2],
            'critical quantity': item[3],
            'brand': item[4],
            'supplier': item[5],
            'catalogue_number': item[6],
            'type': item[7],
            'model': item[8]}
    json[item[0]] = temp
    return json

def worker_items_to_json(data):
    json={}
    for item in data:
        temp = {'name': item[1],
                'quantity': item[2],
                'brand': item[3],
                'type': item[4],
                'model': item[5]}
        json[item[0]] = temp
    return json

def worker_todolist_to_json(data):
    json={}
    for item in data:
        temp = {'machine': item[1],
                'date_of_assignment': item[2],
                'state': item[4],
                'description': item[5]}
        json[item[0]] = temp
    return json

def maintenence_list_to_json(maintenence_list):
    json = {}
    for item in maintenence_list:
        temp = {'name': item[1],
                'frequency of maintenance': item[3],
                'last maintenance': item[4],
                'last maintenance person': item[5]}
        json[item[0]] = temp
    return json