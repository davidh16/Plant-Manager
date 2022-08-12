from model.parts_model import Part

# This function checks if certain part already exists in the warehouse.
# It is necessary because to check if part already exists, we need to check every column of the database

def item_existence(data):
    existance = Part.query.filter_by(part=data['part'],
                    quantity=data['quantity'],
                    critical_quantity=data['critical_quantity'],
                    supplier=data['supplier'],
                    brand=data['brand'],
                    catalogue_number=data['catalogue_number'],
                    type=data['type'],
                    model=data['model']).first()
    if existance:
        return True
    return False