from utils.date_conversion import *
from utils.data_manipulation import *
from utils.user_utils import *
from model.employee_model import Employee
from flask import make_response
import psycopg2 as pg2

file = open('password.txt')
db_password = file.read()

def employee_registration_service(data):
    # funkcija za registraciju zaposlenika, odnosno za umetanje novog red u tablicu 'zaposlenici' baze podataka

    conn = pg2.connect(database='PlantManager', user='postgres', password=db_password)
    cur = conn.cursor()

    cur.execute("SELECT * FROM employees WHERE phone_number = %s", (data['phone_number'],))
    existance = cur.fetchone()

    if existance:
        return make_response({'message':'Employee with the same phone number already exists'})

    created_username = create_nickname(data['name'], data['surname'])
    created_password = generate_password()

    new_employee = Employee(name=data['name'],
                            surname=data['surname'],
                            job=data['job'],
                            access_level=data['access_level'],
                            phone_number=data['phone_number'],
                            income=data['income'],
                            date_of_birth=convert_date(data['date_of_birth']),
                            date_of_employment=convert_date(data['date_of_employment']),
                            username=created_username,
                            password=created_password,
                            )

    cur.execute(
        "INSERT INTO employees(name,surname,access_level,phone_number,date_of_birth,date_of_employment,username,password,income,job) VALUES(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)",
        (new_employee.name, new_employee.surname, new_employee.access_level, new_employee.phone_number,
         new_employee.date_of_birth, new_employee.date_of_employment, new_employee.username, new_employee.password,
         new_employee.income, new_employee.job))
    conn.commit()
    if new_employee.access_level == 'worker':
        conn1 = pg2.connect(database='PlantManager', user='postgres', password=db_password)
        cur1 = conn1.cursor()
        cur1.execute(f'CREATE TABLE workers_tasks.{created_username} (task_id SERIAL PRIMARY KEY, machine VARCHAR, date_of_assignment TIMESTAMP, date_of_completion TIMESTAMP, status VARCHAR, description TEXT, description_of_work TEXT, machine_id INT REFERENCES machines(machine_id))')
        conn1.commit()

    return make_response({'message':"Employee successfully registered"})

def employees_list_service():
    # funkcija za dohvaćanje svih zaposlenika iz baze podataka
    # ova funkcija je potrebna kako bi se mogli prikazati svi zaposlenici na ekranu kada se pritisne gumb 'Zaposlenici'

    conn = pg2.connect(database='PlantManager', user='postgres', password=db_password)
    cur = conn.cursor()
    cur.execute("SELECT id,username,name,surname,job,access_level FROM employees")
    data = cur.fetchall()

    return partial_data_to_json(data), 200

def employee_by_id_service(id):
    # funkcija za dohvažanje podataka o zaposleniku koji se pretražuje putem njegovog id-a
    # ova funkcija je potrebna kako bi se podaci o odabranom zaposleniku prikazali na ekranu prije nego što se isti ažuriraju

    conn = pg2.connect(database='PlantManager', user='postgres', password=db_password)
    cur = conn.cursor()
    cur.execute("SELECT * FROM employees WHERE id = %s",(id,))
    data = cur.fetchall()
    current_emplyoee = retrieved_data_to_json(data)
    return current_emplyoee, 200


def update_employee_service(id, new_data):
    # funkcija izvršava ažuriranje podataka odabranog zaposlenika putem id-a

    conn = pg2.connect(database='PlantManager', user='postgres', password=db_password)
    cur = conn.cursor()
    cur.execute("SELECT * FROM employees WHERE id = %s", (id,))
    data = cur.fetchall()

    if data:
        cur.execute("UPDATE employees SET name = %s, surname = %s, phone_number = %s, job = %s, access_level = %s, date_of_birth = %s, date_of_employment = %s, income = %s WHERE id = %s",
                    (new_data['name'],new_data['surname'],new_data['phone_number'],new_data['job'],new_data['access_level'],convert_date(new_data['date_of_birth']),convert_date(new_data['date_of_employment']),new_data['income'],id))
        conn.commit()
        return make_response({'message': 'Employee successfully updated'})
    return make_response({'message': 'Employee does not exist'})

def employee_delete_service(id):
    # funkcija za brisanje zaposlneika po id-u iz baze podataka


    conn = pg2.connect(database='PlantManager', user='postgres', password=db_password)
    cur = conn.cursor()

    cur.execute("SELECT * FROM employees WHERE id = %s", (id,))
    data = cur.fetchone()

    if data:
        cur.execute("DELETE FROM employees WHERE id = %s", (id,))
        conn.commit()

        return make_response(({'message': 'Employee successfully deleted'}))

    return make_response({'message':'Employee does not exist'})


def emplyee_details_service(user_id):
    return employee_by_id_service(user_id)

