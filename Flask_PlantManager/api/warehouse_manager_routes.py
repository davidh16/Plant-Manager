from flask_restful import request
from service.warehouse_manager_service import new_part_service, get_part_info_service, get_parts_list_service, update_part_service
from flask import Blueprint, make_response
from flask_login import login_required, current_user

warehouse_manager_blueprint = Blueprint('warehouse_manager_blueprint', __name__)

# These routes are for the employee whose access level is 'warehouse_manager'
# His job is to track quantity of certain parts in the warehouse, he also can update every part as well as adding new ones

@warehouse_manager_blueprint.route('/warehouse_manager/item/new', methods=['POST'])
@login_required
def new_item():
    if current_user.access_level != 'warehouse_manager':
        return make_response('401')
    data = request.get_json()
    return new_part_service(data)

@warehouse_manager_blueprint.route('/warehouse_manager/items', methods=['GET'])
@login_required
def items_list():
    if current_user.access_level != 'warehouse_manager':
        return make_response('401')
    return get_parts_list_service()

@warehouse_manager_blueprint.route('/warehouse_manager/update/info/<part_id>', methods=['GET'])
@login_required
def item_info(part_id):
    if current_user.access_level != 'warehouse_manager':
        return make_response('401')
    return get_part_info_service(part_id)

@warehouse_manager_blueprint.route('/warehouse_manager/update/<part_id>', methods=['PUT'])
@login_required
def update(part_id):
    if current_user.access_level != 'warehouse_manager':
        return make_response('401')
    data = request.get_json()
    return update_part_service(part_id, data)