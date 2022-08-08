import psycopg2 as pg2
from datetime import datetime
from utils.data_manipulation import maintenence_list_to_json
from flask import make_response
from model.task_model import Task

file = open('password.txt')
db_password = file.read()

def parts_for_maintenance_service():
    conn=pg2.connect(database='PlantManager',user='postgres',password=db_password)
    cur = conn.cursor()
    cur.execute("SELECT machine_id,machine,needs_frequent_maintenance,frequency_of_maintenance,last_maintenance,last_maintenance_by,last_maintetance + frequency_of_maintenance* INTERVAL'1 day' as date FROM machines")
    data = cur.fetchall()

    maintenence_list = []
    for item in data:
        if item[2] == True and item[6] < datetime.today():
            maintenence_list.append(item)
    return maintenence_list_to_json(maintenence_list)

def task_assignment_service(worker_id,data):
    conn = pg2.connect(database='PlantManager', user='postgres', password=db_password)
    cur = conn.cursor()
    cur.execute("SELECT username,name,surname,access_level  FROM employees WHERE id = %s",(worker_id,))
    worker_info = cur.fetchone()

    new_task = Task(machine = data['machine'],
                    machine_id = data['machine_id'],
                    status = 'In progress',
                    date_of_assignment =  None,
                    date_of_completion = None,
                    description = data['description'],
                    description_of_work = None)

    cur.execute(f"INSERT INTO workers_tasks.{worker_info[0]}(machine,machine_id,date_of_assignment,status,description) VALUES(%s,%s,NOW(),'In progress',%s)",(new_task['machine'],new_task['machine_id'],new_task['description']))
    conn.commit()
    return make_response({'message':f'Task successfully assigned to {worker_info[1]} {worker_info[2]}'})

def tasks_list_service():
    conn = pg2.connect(database='PlantManager', user='postgres', password=db_password)
    cur = conn.cursor()
    cur.execute("SELECT username FROM employees WHERE access_level = 'worker'")
    workers = cur.fetchall()

    tasks_json={}

    for worker in workers:
        cur.execute("SELECT name, surname FROM employees WHERE username = %s",(worker,))
        data=cur.fetchone()
        key = data[0] + " " + data[1]

        cur.execute(f"SELECT * FROM workers_tasks.{worker[0]} WHERE status = 'In progress'")
        tasks = cur.fetchall()
        temp = {}
        for task in tasks:
            temp[task[0]]={'machine' : task[1],
                           'date_of_assignment' : task[2],
                            'status' : task[3],
                           'description':task[5]}
        tasks_json[key] = temp

    return tasks_json
