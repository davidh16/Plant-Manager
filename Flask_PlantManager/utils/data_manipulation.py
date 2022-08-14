from flask import make_response

# These functions are for converting retrieved data into json format
# There are 4 custom functions for converting data about employees, machines, parts and tasks (that are assigned to employees)
# Every function has 2 parts, first parts tries to convert data to json if there are more 'pieces' of data (ie. if there are 2 or more employees)
# second part is for converting 'one piece' data to json if data consists of one 'piece' (ie. of one employee)

def retrieved_employees_to_json(retrieved_data):
    # funkcija koja pretvara povečene podatke iz baze podataka u json format

    if retrieved_data:
        json = {}
        try:
            for item in retrieved_data:
                temp = {'username' : item.username,
                        'name' : item.name,
                        'surname' : item.surname,
                        'job' : item.job,
                        'access_level' : item.access_level,
                        'date_of_employment' : item.date_of_employment,
                        'phone_number' : item.phone_number,
                        'income' : item.income,
                        'date_of_birth' : item.date_of_birth}
                json[item.id] = temp
        except:
            json = {retrieved_data.id : {'username': retrieved_data.username,
                                        'name': retrieved_data.name,
                                        'surname': retrieved_data.surname,
                                        'job': retrieved_data.job,
                                        'access_level': retrieved_data.access_level,
                                        'date_of_employment': retrieved_data.date_of_employment,
                                        'phone_number': retrieved_data.phone_number,
                                        'income': retrieved_data.income,
                                        'date_of_birth': retrieved_data.date_of_birth}}
        return json
    return make_response({'message':'Employee does not exist'})

def retrieved_machines_to_json(retrieved_data):
    if retrieved_data:
        json = {}
        try:
            for item in retrieved_data:
                temp = {'machine': item.machine,
                        'maintenance_freq': item.maintenance_freq,
                        'maintenance_needed': item.maintenance_needed,
                        'last_maintenance': item.last_maintenance,
                        'last_maintenance_by': item.last_maintenance_by}
                json[item.machine_id] = temp
        except:
            json = {retrieved_data.machine_id: {'machine': retrieved_data.machine,
                        'maintenance_freq': retrieved_data.maintenance_freq,
                        'maintenance_needed': retrieved_data.maintenance_needed,
                        'last_maintenance': retrieved_data.last_maintenance,
                        'last_maintenance_by': retrieved_data.last_maintenance_by}}
        return json
    return make_response({'message':'No machines for maintenance'})

def retrieved_parts_to_json(retrieved_data):
    if retrieved_data:
        json = {}
        try:
            for item in retrieved_data:
                temp = {'part': item.part,
                        'quantity': item.quantity,
                        'critical_quantity': item.critical_quantity,
                        'supplier': item.supplier,
                        'brand': item.brand,
                        'type': item.type,
                        'model': item.model,
                        'catalogue_number':item.catalogue_number,
                        'last_administration':item.last_administration,
                        'last_administration_by':item.last_administration_by}
                json[item.part_id] = temp
        except:
            json = {retrieved_data.part_id: {'part': retrieved_data.part,
                        'quantity': retrieved_data.quantity,
                        'critical_quantity': retrieved_data.critical_quantity,
                        'supplier': retrieved_data.supplier,
                        'brand': retrieved_data.brand,
                        'type': retrieved_data.type,
                        'model': retrieved_data.model,
                        'catalogue_number':retrieved_data.catalogue_number,
                        'last_administration':retrieved_data.last_administration,
                        'last_administration_by':retrieved_data.last_administration_by}}
        return json
    return make_response({'message': 'No parts'})

def worker_todolist_to_json(retrieved_data):
    print(retrieved_data)
    if retrieved_data:
        json = {}
        try:
            for item in retrieved_data:
                temp = {'machine': item.machine,
                        'machine_id': item.machine_id,
                        'status': item.status,
                        'date_of_assignment': item.date_of_assignment,
                        'date_of_completion': item.date_of_completion,
                        'description': item.description,
                        'description_of_work': item.description_of_work,
                        'user_id': item.user_id}
                json[item.task_id] = temp
        except:
            json = {retrieved_data[0].task_id: {'machine': retrieved_data[0].machine,
                        'machine_id': retrieved_data[0].machine_id,
                        'in_progress': retrieved_data[0].in_progress,
                        'date_of_assignment': retrieved_data[0].date_of_assignment,
                        'date_of_completion': retrieved_data[0].date_of_completion,
                        'description': retrieved_data[0].description,
                        'description_of_work': retrieved_data[0].description_of_work,
                        'user_id': retrieved_data[0].user_id}}
        return json
    return make_response({'message': 'No tasks'})