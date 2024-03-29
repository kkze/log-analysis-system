from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.cron import CronTrigger
from apscheduler.events import EVENT_JOB_EXECUTED, EVENT_JOB_ERROR 
from flask import current_app
from .task import run_task
from .models import ScheduledTask
scheduler = BackgroundScheduler(daemon=True)

def reload_tasks(app):
    app.logger.info("Reloading tasks...")
    scheduled_jobs = scheduler.get_jobs()
    tasks = ScheduledTask.query.filter_by(status='running').all()

    for task in tasks:
        if f'scheduled_task_{task.id}' not in [job.id for job in scheduled_jobs]:
            app.logger.info(f"Scheduling task {task.id} [{task.name}] with schedule {task.schedule}")
            scheduler.add_job(
                func=run_task,
                args=[task.id, app],
                trigger=CronTrigger.from_crontab(task.schedule),
                id=f'scheduled_task_{task.id}',
                name=task.name,
                replace_existing=True,
            )

def init_scheduler(app):
    with app.app_context():
        reload_tasks(app)
        if not scheduler.running:
            scheduler.start()

    @app.teardown_appcontext
    def shutdown_scheduler(exception=None):
        if scheduler.running:
            app.logger.info("Shutting down scheduler...")
            scheduler.shutdown(wait=False)

#任务执行添加监听器来处理错误和发送通知
def task_listener(event):
    if event.exception:
        current_app.logger.error(f"Task {event.job_id} failed with exception: {event.exception}")
        # 发送通知逻辑...
    else:
        current_app.logger.info(f"Task {event.job_id} completed successfully.")

scheduler.add_listener(task_listener, EVENT_JOB_EXECUTED | EVENT_JOB_ERROR)