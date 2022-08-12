import datetime
from database import db

class Machine(db.Model):
    __tablename__='machines'
    machine_id = db.Column(db.Integer, primary_key=True)
    machine = db.Column('machine', db.String(100))
    maintenance_needed = db.Column('maintenance_needed', db.Boolean)
    last_maintenance_by = db.Column('last_maintenance_by',db.String(100))
    last_maintenance = db.Column('last_maintenance', db.DateTime)
    maintenance_freq = db.Column('maintenance_freq', db.Integer)

    def __init__(self,machine,maintenance_freq):
        self.machine = machine
        self.maintenance_freq = maintenance_freq
        self.maintenance_needed = False
        self.last_maintenance = datetime.datetime.utcnow()