from database import db, login_manager
from flask_login import UserMixin
from sqlalchemy.orm import relationship

@login_manager.user_loader
def load_user(user_id):
    return Employee.query.get(user_id)

class Employee(db.Model, UserMixin):
    __tablename__='employees'
    id = db.Column('id', db.Integer, primary_key=True)
    name = db.Column('name', db.String(100))
    surname = db.Column('surname', db.String(100))
    job = db.Column('job',db.String(100))
    access_level = db.Column('access_level', db.String(100))
    phone_number = db.Column('phone_number',db.String(100))
    date_of_birth = db.Column('date_of_birth', db.DateTime)
    date_of_employment = db.Column('date_of_employment', db.DateTime)
    income = db.Column('income', db.Integer)
    username = db.Column('username', db.String(100), unique=True)
    password = db.Column('password',db.String(100))
    last_login = db.Column('last_login', db.Date)
    last_logout = db.Column('last_logout', db.Date)
    last_warehouse_entrance = db.Column('last_warehouse_entrance', db.Date)
    last_warehouse_exit = db.Column('last_warehouse_exit', db.Date)
    logs = relationship("Log", cascade="all,delete", backref="employees")

    def __init__(self, name, surname, job, access_level, phone_number, date_of_birth, date_of_employment, income, username, password):
        self.name = name
        self.surname = surname
        self.job = job
        self.access_level = access_level
        self.phone_number = phone_number
        self.date_of_birth = date_of_birth
        self.date_of_employment = date_of_employment
        self.income = income
        self.username = username
        self.password = password
