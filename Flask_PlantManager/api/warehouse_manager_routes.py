from flask_restful import request
from service.warehouse_manager_service import *
from flask import Blueprint
from api.token import token_requirement

warehouse_manager_blueprint = Blueprint('warehouse_manager_blueprint', __name__)


@warehouse_manager_blueprint.route('/warehouse_manager/item/new', methods=['POST'])
@token_requirement
def new_item(access_level):
    if access_level != 'warehouse_manager':
        return make_response({"You don't have a permission to perform that action"})
    data = request.get_json()
    return new_item_service(data)

@warehouse_manager_blueprint.route('/warehouse_manager/items', methods=['GET'])
@token_requirement
def items_list(access_level):
    if access_level != 'warehouse_manager':
        return make_response({"You don't have a permission to perform that action"})
    return items_list_service()

@warehouse_manager_blueprint.route('/warehouse_manager/update/info/<item_id>', methods=['GET'])
@token_requirement
def item_info(access_level,item_id):
    if access_level != 'warehouse_manager':
        return make_response({"You don't have a permission to perform that action"})
    return item_info_service(item_id)

@warehouse_manager_blueprint.route('/warehouse_manager/<user_id>/update/<item_id>', methods=['PUT'])
@token_requirement
def update(access_level,item_id, user_id):
    if access_level != 'warehouse_manager':
        return make_response({"You don't have a permission to perform that action"})
    data = request.get_json()
    return update_item_service(item_id, data, user_id)