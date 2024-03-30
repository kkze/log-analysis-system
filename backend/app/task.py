# backend/app/task.py
from datetime import datetime, timezone
from .utils import perform_db_operation
from .log_parser import main as parse_logs
from .models import ScheduledTask, db

# 定义任务映射
TASK_MAPPING = {
    'log_parser': parse_logs,
}

def run_task(task_id, app):
    with app.app_context():  # 显式地为任务执行创建并激活一个新的应用上下文
        task = ScheduledTask.query.get(task_id)
        if task:
            task_func = TASK_MAPPING.get(task.task_type)
            if task_func:
                try:
                    print(f"{task_id} 正在运行")  # 正确使用f-string
                    task_func()
                    task.last_run = datetime.now(timezone.utc)
                    db.session.commit()
                except Exception as e:
                    db.session.rollback()
                    app.logger.error(f"Error executing task {task.id} [{task.task_type}]: {e}")
            else:
                app.logger.warning(f"Task function for {task.task_type} not found.")
