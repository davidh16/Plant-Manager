from database import db
from model.employees_model import Employee
from model.machines_model import Machine

class Task(db.Model):
    __tablename__='tasks'
    task_id = db.Column('task_id', db.Integer, primary_key=True)
    machine=db.Column('machine', db.String(100))
    machine_id=db.Column('machine_id', db.Integer, db.ForeignKey(Machine.machine_id))
    in_progress=db.Column('in_progress',db.Boolean)
    date_of_assignment=db.Column('date_of_assignment',db.DateTime)
    date_of_completion=db.Column('date_of_completion', db.DateTime)
    description=db.Column('description', db.Text)
    description_of_work=db.Column('description_of_work', db.Text)
    user_id = db.Column('user_id',db.Integer, db.ForeignKey(Employee.id))
    assigned_to = db.Column('assigned_to',db.String(100))

    def __init__(self,machine, date_of_assignment,in_progress,description,machine_id,user_id,assigned_to):
        self.machine = machine
        self.date_of_assignment = date_of_assignment
        self.in_progress = in_progress
        self.description = description
        self.machine_id = machine_id
        self.user_id = user_id
        self.assigned_to = assigned_to