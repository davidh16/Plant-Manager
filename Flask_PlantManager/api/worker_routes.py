from flask_restful import request
from service.worker_service import worker_scanner_service,warehouse_list_service,worker_todolist_service,task_done_service
from flask import Blueprint, make_response
from flask_login import login_required, current_user

worker_blueprint = Blueprint('worker_blueprint', __name__)

# These routes are for the employee whose access level is 'worker'
# He can view all the parts available in warehouse and list of tasks which are assigned to him by the shift manager
# There is a route for closing the task which triggers the scanner because it is necessary to scan the machine which has been worked on
# There is also a route just for the scanner which allows the worker to scan whatever he wants and based on what he has scanned he can :
    # enter the warehouse
    # exit the warehouse
    # get a part form the warehouse (updates part table from the database)
    # get the information about the machine

@worker_blueprint.route('/worker/warehouse', methods=['GET'])
@login_required
def warehouse():
    if current_user.access_level != 'worker':
        return make_response('401')
    return warehouse_list_service()

@worker_blueprint.route('/worker/<user_id>/todolist', methods=['GET'])
@login_required
def todolist(user_id):
    print(current_user.access_level)
    if current_user.access_level != 'worker':
        return make_response('401')
    return worker_todolist_service(user_id)

@worker_blueprint.route('/worker/<user_id>/todolist/<task_id>/done', methods=['PUT'])
def task_done(user_id, task_id):
    if current_user.access_level != 'worker':
        return make_response('401')
    data = request.get_json()
    return task_done_service(user_id, task_id, data)

@worker_blueprint.route('/worker/<user_id>/scanner', methods=['PUT'])
def scanner(user_id):
    if current_user.access_level != 'worker':
        return make_response('401')
    data = request.get_json()
    return worker_scanner_service(user_id,data)

