# backend/app/task.py
from datetime import datetime, timezone
from flask import current_app, jsonify

from .utils import perform_db_operation
from .log_parser import main as parse_logs
from .models import ScheduledTask, db

# 定义任务映射
TASK_MAPPING = {
    'log_parser': parse_logs,
}

def run_task(task_id,app):
    with app.app_context():  # 显式地为任务执行创建并激活一个新的应用上下文
        task = ScheduledTask.query.get(task_id)
        if task:
            task_func = TASK_MAPPING.get(task.task_type)
            if task_func:
                try:
                    task_func()
                    task.last_run = datetime.now(timezone.utc)
                    db.session.commit()
                except Exception as e:
                    db.session.rollback()
                    app.logger.error(f"Error executing task {task.id} [{task.task_type}]: {e}")
            else:
                app.logger.warning(f"Task function for {task.task_type} not found.")

def start_task(task_id, app):
    """启动指定ID的任务"""
    task = ScheduledTask.query.get(task_id)
    if not task:
        app.logger.warning(f"Task {task_id} not found.")
        return jsonify({"error": "Task not found."}), 404
    
    if task.status == 'running':
        app.logger.info(f"Task {task_id} is already running.")
        return jsonify({"message": "Task is already running."}), 400
    
    task.status = 'running'
    return perform_db_operation(
        lambda: db.session.commit(),
        "Task started successfully.",
        f"Failed to start task {task_id}."
    )

def stop_task(task_id, app):
    """停止指定ID的任务"""
    task = ScheduledTask.query.get(task_id)
    if not task:
        app.logger.warning(f"Task {task_id} not found.")
        return jsonify({"error": "Task not found."}), 404
    
    if task.status == 'stopped':
        app.logger.info(f"Task {task_id} is already stopped.")
        return jsonify({"message": "Task is already stopped."}), 400
    
    task.status = 'stopped'
    return perform_db_operation(
        lambda: db.session.commit(),
        "Task stopped successfully.",
        f"Failed to stop task {task_id}."
    )