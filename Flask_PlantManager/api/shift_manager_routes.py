from flask import Blueprint, make_response
from flask_restful import request
from service.shift_manager_service import get_maintenance_list_service,get_tasks_list_service,\
                                        get_workers_list_service,task_assignment_service,new_machine_service
from flask_login import login_required,current_user

shift_manager_blueprint = Blueprint('shift_manager_blueprint', __name__)

# These routes are routes related to the user whose access level is 'shift manager'
# His job is to track which machines are in need of maintenance and he assignes tasks to workers to maintain certain machines

@shift_manager_blueprint.route('/shiftmanager/maintenance', methods=['GET'])
@login_required
def maintenance():
    if current_user.access_level != 'shift_manager':
        return make_response('401')
    return get_maintenance_list_service()

@shift_manager_blueprint.route('/shiftmanager/workers_list', methods=['GET'])
@login_required
def workers_list():
    if current_user.access_level != 'shift_manager':
        return make_response('401')
    return get_workers_list_service()

@shift_manager_blueprint.route('/shiftmanager/maintenance/task/<user_id>', methods=['POST'])
def task_assignment(user_id):
    data = request.get_json()
    return task_assignment_service(user_id,data)

@shift_manager_blueprint.route('/shiftmanager/tasks', methods=['GET'])
@login_required
def tasks_list():
    if current_user.access_level != 'shift_manager':
        return make_response('401')
    return get_tasks_list_service()

@shift_manager_blueprint.route('/shiftmanager/new_machine', methods=['POST'])
@login_required
def new_machine():
    if current_user.access_level != 'shift_manager':
        return make_response('401')
    data = request.get_json()
    return new_machine_service(data)