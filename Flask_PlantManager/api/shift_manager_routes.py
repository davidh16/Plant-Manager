from flask import Blueprint
from flask_restful import request
from service.shift_manager_service import *
from api.token import token_requirement

shift_manager_blueprint = Blueprint('shift_manager_blueprint', __name__)


@shift_manager_blueprint.route('/shiftmanager/maintenance', methods=['GET'])
@token_requirement
def maintenance(access_level):
    if access_level != 'shiftmanager':
        return make_response({"You don't have a permission to perform that action"})
    return parts_for_maintenance_service()

@shift_manager_blueprint.route('/shiftmanager/maintenance/task/<worker_id>', methods=['POST'])
@token_requirement
def task_assignment(access_level,worker_id):
    if access_level != 'shiftmanager':
        return make_response({"You don't have a permission to perform that action"})
    data = request.get_json()
    return task_assignment_service(worker_id,data)

@shift_manager_blueprint.route('/shiftmanager/tasks', methods=['GET'])
@token_requirement
def tasks_list(access_level):
    if access_level != 'shiftmanager':
        return make_response({"You don't have a permission to perform that action"})
    return tasks_list_service()
