import psycopg2 as pg2
from utils.data_manipulation import worker_items_to_json, worker_todolist_to_json
from flask import make_response

file = open('password.txt')
db_password = file.read()

def warehouse_list_service():
    conn = pg2.connect(database='PlantManager',user='postgres',password=db_password)
    cur = conn.cursor()
    cur.execute("SELECT part_id,part,quantity,brand,type,model FROM warehouse")

    data = cur.fetchall()
    return worker_items_to_json(data)

def worker_todolist_service(user_id):
    conn = pg2.connect(database='PlantManager', user='postgres', password=db_password)
    cur = conn.cursor()
    cur.execute("SELECT username FROM employees WHERE id =%s",(user_id,))
    username = cur.fetchone()
    cur.execute(f"SELECT * FROM workers_tasks.{username} WHERE status = 'In progress'")

    data = cur.fetchall()

    return worker_todolist_to_json(data)

def task_done_service(user_id,task_id,data):
    conn = pg2.connect(database='PlantManager', user='postgres', password=db_password)
    cur = conn.cursor()
    cur.execute("SELECT username FROM employees WHERE id = %s",(user_id,))
    username = cur.fetchone()[0]

    cur.execute(f"SELECT machine_id FROM workers_tasks.{username} WHERE task_id = %s",(task_id,))
    assigned_machine = cur.fetchone()[0]

    if data['scanned_machine'] == assigned_machine and data['work_description']:
        cur.execute(f"UPDATE workers_tasks.{username} SET status = 'Done', date_of_completion = NOW(), description_of_work = %s WHERE task_id = %s",(data['work_description'],task_id))
        conn.commit()

        cur.execute("UPDATE machines SET last_maintenance = NOW(), last_maintained_by = %s , in_need_of_maintenance = 'False' WHERE machine_id = %s",(username,assigned_machine))
        conn.commit()

        return make_response({'message':'Task done'})
    return make_response({'message':'It is necessary to scan correct machine you are working on and fill in your work description'})