from model.item_model import Item
from utils.item_existence import item_existence
from utils.data_manipulation import *
from flask import make_response
import psycopg2 as pg2

file = open('password.txt')
db_password = file.read()

def new_item_service(data):

    existance = item_existence(data)

    if existance == True:
        return make_response({'message':'Item already exists'})

    new_item = Item(name=data['name'],
                    quantity=data['quantity'],
                    critical_quantity=data['critical_quantity'],
                    supplier=data['supplier'],
                    brand=data['brand'],
                    catalogue_number=data['catalogue_number'],
                    type=data['type'],
                    model=data['model'])

    conn = pg2.connect(database='PlantManager', user='postgres', password=db_password)
    cur = conn.cursor()
    cur.execute('INSERT INTO warehouse(part,quantity,critical_quantity,supplier,brand,type,model,catalogue_number) VALUES(%s,%s,%s,%s,%s,%s,%s,%s)',
                (new_item.name,new_item.quantity,new_item.critical_quantity,new_item.supplier,new_item.brand,new_item.type,new_item.model,new_item.catalogue_number))
    conn.commit()

    return make_response({'message':'Item successfully added'})

def items_list_service():
    conn = pg2.connect(database='PlantManager', user='postgres', password=db_password)
    cur = conn.cursor()
    cur.execute('SELECT * FROM warehouse')
    data = cur.fetchall()
    return retrieved_items_to_json(data)

def item_info_service(id):
    conn = pg2.connect(database='PlantManager', user='postgres', password=db_password)
    cur = conn.cursor()
    cur.execute('SELECT * FROM warehouse WHERE part_id = %s',(id,))
    data = cur.fetchone()
    print(data)
    return item_to_json(data)

def update_item_service(item_id, new_data, user_id):
    conn = pg2.connect(database='PlantManager', user='postgres', password=db_password)
    cur = conn.cursor()
    cur.execute("SELECT * FROM warehouse WHERE part_id = %s", (item_id,))
    data = cur.fetchall()

    if data:
        cur.execute(
            "UPDATE warehouse SET part = %s, quantity = %s, critical_quantity = %s, brand = %s, supplier = %s, catalogue_number = %s, type = %s, model = %s WHERE part_id = %s",
            (new_data['name'], new_data['quantity'], new_data['critical_quantity'], new_data['brand'],
             new_data['supplier'], new_data['catalogue_number'],
             new_data['type'], new_data['model'], item_id))
        conn.commit()

        cur.execute("SELECT name,surname FROM employees WHERE id = %s",(user_id,))
        data = cur.fetchone()

        cur.execute("UPDATE warehouse SET last_administration = NOW(), last_administration_by = %s WHERE part_id = %s",(data[0] + " " +data[1],item_id))
        conn.commit()
        return make_response({'message': 'Item successfully updated'})
    return make_response({'message': 'Item does not exist'})