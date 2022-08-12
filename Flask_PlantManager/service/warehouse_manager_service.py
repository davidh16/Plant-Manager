from flask import make_response
from flask_login import current_user
import datetime
from database import db
from qrcode_maker import qr_code_part
from model.parts_model import Part
from utils.item_existence import item_existence
from utils.data_manipulation import retrieved_parts_to_json

def new_part_service(data):
    existance = item_existence(data)
    if existance:
        return make_response({'message':'Item already exists'})
    new_part = Part(part=data['part'],
                    quantity=data['quantity'],
                    critical_quantity=data['critical_quantity'],
                    supplier=data['supplier'],
                    brand=data['brand'],
                    catalogue_number=data['catalogue_number'],
                    type=data['type'],
                    model=data['model'])
    db.session.add(new_part)
    db.session.commit()
    qr_code_part(new_part.part_id)
    return make_response({'message':'Item successfully added'})

def get_parts_list_service():
    parts = Part.query.all()
    return retrieved_parts_to_json(parts)

def get_part_info_service(part_id):
    part = Part.query.filter_by(part_id=part_id).first()
    return retrieved_parts_to_json(part)

def update_part_service(part_id, new_data):
    part = Part.query.filter_by(part_id=part_id).first()
    if part:
        part.part = new_data['part']
        part.quantity = part.quantity + new_data['quantity']
        part.critical_quantity = new_data['critical_quantity']
        part.brand = new_data['brand']
        part.supplier = new_data['supplier']
        part.catalogue_number = new_data['catalogue_number']
        part.type = new_data['type']
        part.model = new_data['model']
        part.last_administration = datetime.datetime.utcnow()
        part.last_administration_by = current_user.username
        db.session.commit()
        return make_response({'message': 'Item successfully updated'})
    return make_response({'message': 'Item does not exist'})