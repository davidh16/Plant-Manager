import datetime
from flask import make_response
from pyzbar.pyzbar import decode
import cv2
from database import db
from model.parts_model import Part
from model.tasks_model import Task
from model.employees_model import Employee
from model.machines_model import Machine
from model.logs_model import Log
from utils.data_manipulation import retrieved_parts_to_json, worker_todolist_to_json, retrieved_machines_to_json

def warehouse_list_service():
    parts = Part.query.all()
    return retrieved_parts_to_json(parts)

def worker_todolist_service(user_id):
    tasks = Task.query.filter_by(user_id=user_id,in_progress=True).all()
    return worker_todolist_to_json(tasks)

def scanner():
    # Normally, this function would trigger the camera of the workers phone but in this case it triggers the webcam
    # Therefore for us to test this scanner function, it is necessary to show QR code to the webcam using phone screen or something similar
    # QR codes are located in directories 'qr_codes_machines' and 'qr_codes_parts'
    # Also, function does not open up the camera window because it would raise an error which I just could not solve

    cap = cv2.VideoCapture(0)
    while True:
        _, frame = cap.read()
        data = decode(frame)
        if data:
            break
    decoded_data = data[0][0].decode().split(",")
    json = {decoded_data[0]: decoded_data[1], decoded_data[2]:decoded_data[3]}
    return json

def worker_scanner_service(user_id,data):
    worker = Employee.query.filter_by(id=user_id).first()
    scanned_object = scanner()
    if scanned_object['type'] == 'part':
        if data:
            part = Part.query.filter_by(part_id=scanned_object['part_id']).first()
            part.quantity -= 1
            part.last_administration_by = worker.username
            db.session.commit()
            new_log = Log(part_id=scanned_object['part_id'],
                          part = part.part,
                          user_id=user_id,
                          user=worker.username,
                          name=worker.name,
                          surname=worker.surname,
                          reason=data['reason'])
            db.session.add(new_log)
            db.session.commit()
            return make_response({'message': f'Part assigned to {worker.name} {worker.surname} use it wisely'})
        return make_response({'message':'To use this part you have to specify what do you need it for'})
    elif scanned_object['type'] == 'machine':
        machine = Machine.query.filter_by(machine_id=scanned_object['machine_id']).first()
        return make_response({'message':{'Scanned object is not a part': retrieved_machines_to_json(machine)}})
    elif scanned_object['type'] == 'warehouse_entrance':
        worker.last_warehouse_entrance = datetime.datetime.utcnow()
        db.session.commit()
        return make_response({'message':'You have entered the warehouse'})
    elif scanned_object['type'] == 'warehouse_exit':
        worker.last_warehouse_exit = datetime.datetime.utcnow()
        db.session.commit()
        return make_response({'message': 'You have exited the warehouse'})

def task_done_service(user_id,task_id,data):
    worker = Employee.query.filter_by(id=user_id).first()
    task = Task.query.filter_by(task_id=task_id).first()
    machine = Machine.query.filter_by(machine_id=task.machine_id).first()

    scanned_machine = scanner()

    if scanned_machine['type'] != 'machine':
        return make_response({'message':'Scanned object is not a machine'})
    if scanned_machine['machine_id'] != task.machine_id:
        return make_response({'message':'Scanned machine is not the machine that is assigned for maintenance in this task'})
    if not data['description_of_work']:
        return make_response({'message':'It is necessary to write what has been done on this machine'})

    task.in_progress = False
    task.date_of_completion = datetime.datetime.utcnow()
    task.description_of_work = data['description_of_work']
    machine.last_maintenance = datetime.datetime.utcnow()
    machine.last_maintenance_by = worker.name + " " + worker.surname
    machine.maintenance_needed = False
    db.session.commit()

    return make_response({'message':'Task successfully done'})