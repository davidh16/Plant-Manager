from flask_restful import request
from service.worker_service import *
from flask import Blueprint
from api.token import token_requirement


worker_blueprint = Blueprint('worker_blueprint', __name__)


@worker_blueprint.route('/worker/warehouse', methods=['GET'])
@token_requirement
def warehouse(access_level):
    if access_level != 'worker':
        return make_response({"You don't have a permission to perform that action"})
    return warehouse_list_service()

@worker_blueprint.route('/worker/<user_id>/todolist', methods=['GET'])
@token_requirement
def todolist(access_level,user_id):
    if access_level != 'worker':
        return make_response({"You don't have a permission to perform that action"})
    return worker_todolist_service(user_id)

@worker_blueprint.route('/worker/<user_id>/todolist/<task_id>/done', methods=['PUT'])
@token_requirement
def task_done(access_level,user_id, task_id):
    if access_level != 'worker':
        return make_response({"You don't have a permission to perform that action"})
    data = request.get_json()
    return task_done_service(user_id, task_id, data)