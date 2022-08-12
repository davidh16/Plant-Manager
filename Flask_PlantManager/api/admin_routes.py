from flask_restful import request
from flask import Blueprint, make_response
from service.admin_service import get_employee_by_id_service, get_employees_list_service,employee_delete_service,\
                                    update_employee_service, employee_registration_service
from flask_login import login_required, current_user

admin_blueprint = Blueprint('admin_blueprint', __name__)

# These routes are for the employee whose access level is 'admin', this kind of access level would have someone who works in HR
# Admin can register, update and delete employees, there are routes for getting details of a specific employee and employees list as well

@admin_blueprint.route('/admin/register/employee', methods=['POST'])
@login_required
def register_employee():
    if current_user.access_level != 'admin':
        return make_response('401')
    data = request.get_json()
    return employee_registration_service(data)

@admin_blueprint.route('/admin/employees', methods = ['GET'])
@login_required
def employees_list():
    if current_user.access_level != 'admin':
        return make_response('401')
    return get_employees_list_service()

@admin_blueprint.route('/admin/employees/update/<user_id>/', methods = ['PUT'])
@login_required
def save_update(user_id):
    if current_user.access_level != 'admin':
        return make_response('401')
    data = request.get_json()
    return update_employee_service(user_id, data)

@admin_blueprint.route('/admin/employees/delete/<user_id>', methods = ['DELETE'])
@login_required
def delete(user_id):
    if current_user.access_level != 'admin':
        return make_response('401')
    return employee_delete_service(user_id)

@admin_blueprint.route('/admin/employees/details/<user_id>', methods = ['GET'])
@login_required
def details(user_id):
    if current_user.access_level != 'admin':
        return make_response('401')
    return get_employee_by_id_service(user_id)


