from model.employees_model import Employee
from database import db

david = Employee.query.filter_by(id=1).first()
david.access_level = 'admin'
db.session.commit()




