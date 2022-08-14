from datetime import datetime
from flask import make_response
from database import db
from qrcode_maker import qr_code_machine
from utils.data_manipulation import retrieved_machines_to_json, retrieved_employees_to_json
from model.tasks_model import Task
from model.machines_model import Machine
from model.employees_model import Employee

def get_maintenance_list_service():
    machines_for_maintenance = Machine.query.filter_by(maintenance_needed=True).all()
    return retrieved_machines_to_json(machines_for_maintenance)

def get_workers_list_service():
    workers = Employee.query.filter_by(access_level='worker').all()
    return retrieved_employees_to_json(workers)

def task_assignment_service(user_id,data):
    assigned_to = Employee.query.filter_by(id=user_id).first()
    assigned_machine = Machine.query.filter_by(machine_id=data['machine_id']).first()
    new_task = Task(machine=assigned_machine.machine,
                    machine_id = data['machine_id'],
                    in_progress = True,
                    date_of_assignment =  datetime.utcnow(),
                    description = data['description'],
                    user_id = user_id,
                    assigned_to=assigned_to.username)
    db.session.add(new_task)
    db.session.commit()
    return make_response({'message':f'Task successfully assigned to {assigned_to.name} {assigned_to.surname}'})

def get_tasks_list_service():
    workers = Employee.query.filter_by(access_level='worker').all()
    tasks_json={}
    for worker in workers:
        key = worker.name + " " + worker.surname
        tasks = Task.query.filter_by(user_id=worker.id, in_progress=True)
        temp = {}
        for task in tasks:
            temp[task.task_id]={'machine' : task.machine,
                                'machine_id': task.machine_id,
                                'in_progress':task.in_progress,
                                'date_of_assignment':task.date_of_assignment,
                                'date_of_completion':task.date_of_completion,
                                'description':task.description,
                                'description_of_work':task.description_of_work,
                                'user_id':task.user_id,
                                'assigned_to':task.assigned_to}
        tasks_json[key] = temp
    if tasks_json == {}:
        return make_response({'message':'All tasks are done'})
    return tasks_json

def new_machine_service(data):
    new_machine = Machine(machine = data['machine'],
                          maintenance_freq= data['maintenance_freq'])
    db.session.add(new_machine)
    db.session.commit()
    qr_code_machine(new_machine.machine_id)
    return make_response({'message':'New machine successfully added'})
