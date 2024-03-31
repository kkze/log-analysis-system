# backend/app/task.py
from datetime import datetime
# from croniter import croniter
import pytz
from .log_parser import main as parse_logs
from .models import ScheduledTask, db
# from .utils import repeat_to_cron

# 定义任务映射
TASK_MAPPING = {
    'single': parse_logs,
    'repeat': parse_logs, 
}

def run_task(task_id, app):
    with app.app_context():
        task = ScheduledTask.query.get(task_id)
        if task:
            task_func = TASK_MAPPING.get(task.task_type)
            if task_func:
                try:
                    tz = pytz.timezone('Asia/Shanghai')  # 为北京时间定义时区
                    now = datetime.now(tz)  # 获取当前时间，并应用时区
                    print(f"{task_id} 正在运行")
                    task_func()
                    task.last_run = datetime.now(pytz.timezone('Asia/Shanghai'))
                    if task.task_type == 'single':
                        task.status = "completed"
                    db.session.commit()
                except Exception as e:
                    db.session.rollback()
                    app.logger.error(f"Error executing task {task.id} [{task.task_type}]: {e}")