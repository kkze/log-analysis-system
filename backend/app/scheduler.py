import atexit
from datetime import datetime
from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.cron import CronTrigger
from apscheduler.events import EVENT_JOB_EXECUTED, EVENT_JOB_ERROR 
from croniter import croniter
from flask import current_app
import pytz
from .utils import generate_scheduler_params, repeat_to_cron
from .task import run_task
from .models import ScheduledTask, TaskExecutionLog
from .models import db

scheduler = BackgroundScheduler(daemon=True)

def reload_tasks(app):
    with app.app_context():
        app.logger.info("Reloading tasks...")
        scheduled_jobs = scheduler.get_jobs()
        tasks = ScheduledTask.query.filter_by(status='running').all()
        for task in tasks:
            scheduler_params = generate_scheduler_params(task.task_type,task.execute_type, task.schedule, task.start_time,task.day_of_week)
            app.logger.info(f"Task {task.id} [{task.name}] is running. scheduler_params: {scheduler_params}")
            if f'scheduled_task_{task.id}' not in [job.id for job in scheduled_jobs]:
                scheduler.add_job(
                    func=run_task,
                    args=[task.id, current_app._get_current_object()],
                    **scheduler_params,
                    id=f'scheduled_task_{task.id}',
                    name=task.name,
                    replace_existing=True,
                )

def init_scheduler(app):
    with app.app_context():
        # 使用lambda函数添加监听器,因为监听器需要在应用上下文中运行
        scheduler.add_listener(lambda event: task_listener(event, app), EVENT_JOB_EXECUTED | EVENT_JOB_ERROR)
        reload_tasks(app)
        if not scheduler.running:
            scheduler.start()
            
    def shutdown_scheduler():
        if scheduler.running:
            scheduler.shutdown()
            print("Shutdown Scheduler...")

    atexit.register(shutdown_scheduler)


#任务执行添加监听器来处理错误和发送通知
def task_listener(event, app):
    with app.app_context():
        task_id = int(event.job_id.split('_')[-1])
        task = ScheduledTask.query.get(task_id)
        if task:
            tz = pytz.timezone('Asia/Shanghai')  # 为北京时间定义时区
            now = datetime.now(tz)  # 获取当前时间，并应用时区
            if task.schedule:
                job = scheduler.get_job(event.job_id)
                task.next_run = job.next_run_time
                print(f"下次运行时间:{job.next_run_time}")



            # 记录任务执行日志
            if event.exception:
                log_entry = TaskExecutionLog(task_id=task.id, executed_at=now, was_successful=False, message=str(event.exception))
            else:
                log_entry = TaskExecutionLog(task_id=task.id, executed_at=now, was_successful=True, message="Task completed successfully.")

            db.session.add(log_entry)
            db.session.commit()