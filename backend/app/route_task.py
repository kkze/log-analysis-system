from flask import request, jsonify
from flask_jwt_extended import jwt_required
from .schemas import TaskSchema
from .utils import perform_db_operation
from .scheduler import reload_tasks
from .models import ScheduledTask, TaskExecutionLog, db  # 使用相对导入
from flask import request, jsonify, Blueprint
from flask_jwt_extended import jwt_required
from marshmallow import Schema, fields, ValidationError, validate
from flask import current_app
bp_task = Blueprint('tasks', __name__)


task_schema = TaskSchema()


@bp_task.route('', methods=['POST'])
@jwt_required()
def create_task():
    try:
        data = task_schema.load(request.get_json())
    except ValidationError as err:
        return jsonify(err.messages), 400
    task = ScheduledTask(
        name=data['name'],
        task_type=data['task_type'],
        status='running',  # 默认状态为pending
        schedule=data.get('schedule'),
        start_time=data.get('start_time'),
        execute_type=data.get('execute_type')
    )
    print(f"Task:{task.to_dict()}")
    db.session.add(task)
    response = perform_db_operation(
        lambda: db.session.commit(),
        "任务创建成功。",
        "任务创建失败。"
    )
    if response.status_code == 200:
        print(f"Success:{response}")
        reload_tasks(current_app._get_current_object())
    return response

@bp_task.route('/<int:task_id>', methods=['PUT'])
@jwt_required()
def edit_task(task_id):
    """
    编辑指定ID的任务。
    """
    task = ScheduledTask.query.get(task_id)
    if not task:
        return jsonify({"error": "任务未找到。"}), 404

    try:
        data = task_schema.load(request.get_json())
    except ValidationError as err:
        return jsonify(err.messages), 400

    task.name = data.get('name', task.name)
    task.task_type = data.get('task_type', task.task_type)
    task.execute_type = data.get('execute_type', task.execute_type)
    task.schedule = data.get('schedule', task.schedule)
    task.start_time = data.get('start_time', task.start_time)

    response = perform_db_operation(
        lambda: db.session.commit(),
        "任务编辑成功。",
        "任务编辑失败。"
    )

    if response.status_code == 200:
        reload_tasks(current_app._get_current_object())
    return response

@bp_task.route('/<int:task_id>', methods=['DELETE'])
@jwt_required()
def delete_task(task_id):
    """
    删除指定ID的任务。
    """
    task = ScheduledTask.query.get(task_id)
    if not task:
        return jsonify({"error": "任务未找到。"}), 404

    db.session.delete(task)
    response = perform_db_operation(
        lambda: db.session.commit(),
        "任务删除成功。",
        "任务删除失败。"
    )

    if response.status_code == 200:
        reload_tasks(current_app._get_current_object())
    return response

@bp_task.route('/start/<int:task_id>', methods=['POST'])
@jwt_required()
def start_task(task_id):
    """
    启动指定ID的任务。
    """
    task = ScheduledTask.query.get(task_id)
    if not task:
        return jsonify({"error": "任务未找到。"}), 404

    if task.status != 'running':
        task.status = 'running'
        response = perform_db_operation(
            lambda: db.session.commit(),
            "任务启动成功。",
            "任务启动失败。"
        )
        if response.status_code == 200:
            reload_tasks(current_app._get_current_object())
            return jsonify({"message": "任务已启动"}), 200
    else:
        return jsonify({"message": "任务已经在运行中。"}), 400

@bp_task.route('/stop/<int:task_id>', methods=['POST'])
@jwt_required()
def stop_task(task_id):
    """
    停止指定ID的任务。
    """
    task = ScheduledTask.query.get(task_id)
    if not task:
        return jsonify({"error": "任务未找到。"}), 404

    if task.status != 'stopped':
        task.status = 'stopped'
        response = perform_db_operation(
            lambda: db.session.commit(),
            "任务停止成功。",
            "任务停止失败。"
        )
        if response.status_code == 200:
            reload_tasks(current_app._get_current_object())
            return jsonify({"message": "任务已停止"}), 200
    else:
        return jsonify({"message": "任务已经停止。"}), 400

@bp_task.route('/list', methods=['GET'])
@jwt_required()
def list_tasks():
    """
    列出所有任务。
    """
    tasks = ScheduledTask.query.all()
    return jsonify([task.to_dict() for task in tasks]), 200

@bp_task.route('/<int:task_id>', methods=['GET'])
@jwt_required()
def get_task(task_id):
    """
    获取指定ID的任务详情。
    """
    task = ScheduledTask.query.get(task_id)
    if not task:
        return jsonify({"error": "任务未找到。"}), 404

    return jsonify(task.to_dict()), 200

@bp_task.route('/<int:task_id>/history', methods=['GET'])
@jwt_required()
def get_task_history(task_id):
    """
    获取指定ID的任务执行历史。
    """
    task = ScheduledTask.query.get(task_id)
    if not task:
        return jsonify({"error": "任务未找到。"}), 404
    
    logs = TaskExecutionLog.query.filter_by(task_id=task_id).all()
    log_entries = [{
        "executed_at": log.executed_at,
        "was_successful": log.was_successful,
        "message": log.message
    } for log in logs]

    return jsonify(log_entries), 200