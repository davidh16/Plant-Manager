import string
import random
from model.employees_model import Employee

def generate_password():
    characters = list(string.ascii_letters + string.digits + "!@#$%")
    lenght = 8
    random.shuffle(characters)
    password = []
    for i in range(lenght):
        password.append(random.choice(characters))
    random.shuffle(password)
    generated_password = "".join(password)
    return generated_password

def create_username(ime,prezime):
    created_username = ime.lower() + prezime.lower()[0]
    employee = Employee.query.filter_by(username=created_username).first()
    i=1
    if employee:
        created_username += str(i)
        employee = Employee.query.filter_by(username=created_username).first()
    while employee :
        created_username = created_username.replace(str(i),str(i+1))
        i += 1
        employee = Employee.query.filter_by(username=created_username).first()
    return created_username
