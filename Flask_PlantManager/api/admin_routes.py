from flask_restful import request
from service.admin_service import *
from flask import Blueprint, make_response
from api.token import token_requirement


admin_blueprint = Blueprint('admin_blueprint', __name__)

@admin_blueprint.route('/admin/register/employee', methods=['POST'])
@token_requirement
def register_employee(access_level):
    if access_level != 'admin':
        return make_response({"You don't have a permission to perform that action"})
    data = request.get_json()
    return employee_registration_service(data)

@admin_blueprint.route('/admin/employees', methods = ['GET'])
@token_requirement
def employees_list(access_level):
    if access_level != 'admin':
        return make_response({"You don't have a permission to perform that action"})
    return employees_list_service()

@admin_blueprint.route('/admin/employees/update/info/<user_id>', methods = ['GET'])
@token_requirement
def update(access_level,user_id):
    if access_level != 'admin':
        return make_response({"You don't have a permission to perform that action"})
    return employee_by_id_service(user_id)

@admin_blueprint.route('/admin/employees/update/<user_id>/', methods = ['PUT'])
@token_requirement
def save_update(access_level,user_id):
    if access_level != 'admin':
        return make_response({"You don't have a permission to perform that action"})
    data = request.get_json()
    return update_employee_service(user_id, data)

@admin_blueprint.route('/admin/employees/delete/<user_id>', methods = ['DELETE'])
@token_requirement
def delete_confirm(access_level,user_id):
    if access_level != 'admin':
        return make_response({"You don't have a permission to perform that action"})
    return employee_delete_service(user_id)

@admin_blueprint.route('/admin/employees/details/<user_id>', methods = ['GET'])
@token_requirement
def employee_details(access_level,user_id):
    if access_level != 'admin':
        return make_response({"You don't have a permission to perform that action"})
    return emplyee_details_service(user_id)


