import datetime
from flask import make_response
from database import db
from utils.user_utils import generate_password, create_username
from utils.date_conversion import convert_date
from utils.data_manipulation import retrieved_employees_to_json
from model.employees_model import Employee

def employee_registration_service(data):
    # This function, after it checks if user already exists, creates new employee and puts it in a database table 'employees'

    user_existance = Employee.query.filter_by(phone_number = data['phone_number']).first()
    if user_existance:
        return make_response({'message':'Employee with the same phone number already exists'})
    created_username = create_username(data['name'], data['surname'])
    generated_password = generate_password()
    new_employee = Employee(
                            name=data['name'],
                            surname=data['surname'],
                            job=data['job'],
                            access_level=data['access_level'],
                            phone_number=data['phone_number'],
                            income=data['income'],
                            date_of_birth=datetime.datetime.now(),
                            date_of_employment=datetime.datetime.now(),
                            username=created_username,
                            password=generated_password,
                            )
    db.session.add(new_employee)
    db.session.commit()

    # Normaly I would make a function that sends login data to the new employee over the SMS hence there is phone number of every employee,
    # but that service is paid so it doesn't make sense for me to use it because this is not commercial app.
    # Therefore I printed login data in response so I (or you) can write it down and change it later like real life employee would.

    return make_response(f"Employee {created_username} successfully registered.\nPlease notify {new_employee.name} {new_employee.surname} that his login data is :\n username : {created_username}\npassword : {p}.\nThis password is temporary and employee should change it.")

def get_employees_list_service():
    # This function returns all employees that are in database

    data = Employee.query.all()
    return retrieved_employees_to_json(data)

def get_employee_by_id_service(id):
    # This function returns data about specific employee who is searched for by his unique id

    data = Employee.query.filter_by(id=id).first()
    return retrieved_employees_to_json(data)

def update_employee_service(user_id, new_data):
    # This function updates data about specific employee who is searched for by his unique id

    employee = Employee.query.filter_by(id=user_id).first()
    if employee:
        employee.name = new_data['name']
        employee.surname = new_data['surname']
        employee.job = new_data['job']
        employee.phone_number = new_data['phone_number']
        employee.access_level = new_data['access_level']
        employee.date_of_birth = convert_date(new_data['date_of_birth'])
        employee.date_of_employment = convert_date(new_data['date_of_employment'])
        employee.income = new_data['income']
        db.session.commit()
        return make_response({'message': 'Employee successfully updated'})
    return make_response({'message': 'Employee does not exist'})

def employee_delete_service(id):
    # This function deletes specific employee who is searched for by his unique id

    employee = Employee.query.filter_by(id=id).first()
    if employee:
        db.session.delete(employee)
        db.session.commit()
        return make_response(({'message': 'Employee successfully deleted'}))
    return make_response({'message': 'Employee does not exist'})

