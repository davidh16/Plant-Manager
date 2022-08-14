from database import db
from sqlalchemy.orm import relationship

class Part(db.Model):
    __tablename__ = 'parts'
    part_id = db.Column('part_id', db.Integer, primary_key=True)
    part = db.Column('part', db.String(100))
    quantity = db.Column('quantity', db.Integer)
    critical_quantity = db.Column('critical_quantity', db.Integer)
    supplier = db.Column('supplier', db.String(100))
    brand = db.Column('brand', db.String(100))
    type= db.Column('type', db.String(100))
    model = db.Column('model', db.String(100))
    catalogue_number = db.Column('catalogue_number', db.String(100))
    last_administration = db.Column('last_administration', db.Date)
    last_administration_by = db.Column('last_administration_by', db.String(100))
    logs = relationship("Log", cascade="all,delete", backref="parts")

    def __init__(self,part, quantity, critical_quantity, supplier, brand, type, model, catalogue_number):
        self.part = part
        self.quantity = quantity
        self.critical_quantity = critical_quantity
        self.supplier = supplier
        self.brand = brand
        self.type = type
        self.model = model
        self.catalogue_number = catalogue_number