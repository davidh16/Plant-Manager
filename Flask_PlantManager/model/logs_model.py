from database import db
from model.employees_model import Employee
from model.parts_model import Part
import datetime

class Log(db.Model):
    __tablename__='logs'
    log_id = db.Column(db.Integer, primary_key=True)
    time = db.Column(db.Date)
    part_id = db.Column(db.Integer, db.ForeignKey(Part.part_id))
    part = db.Column(db.String(100))
    user_id = db.Column(db.Integer, db.ForeignKey(Employee.id))
    user = db.Column(db.String(100))
    name = db.Column(db.String(100))
    surname = db.Column(db.String(100))
    reason = db.Column(db.Text)

    def __init__(self,part_id,part,user_id,user,name,surname,reason):
        self.time = datetime.datetime.utcnow()
        self.part_id = part_id
        self.part = part
        self.user_id = user_id
        self.user = user
        self.name = name
        self.surname = surname
        self.reason = reason

