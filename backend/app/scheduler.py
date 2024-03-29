# backend/app/scheduler.py
from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.cron import CronTrigger
from .models import ScheduledTask
from .log_parser import main as parse_logs

scheduler = BackgroundScheduler(daemon=True)

def reload_tasks(app):
    with app.app_context():
        scheduler.remove_all_jobs()  # 清除现有的任务
        tasks = ScheduledTask.query.filter_by(status='running').all()
        for task in tasks:
            scheduler.add_job(
                func=parse_logs,
                trigger=CronTrigger.from_crontab(task.schedule),
                id=str(task.id),
                name=task.name
            )

def init_scheduler(app):
    with app.app_context():
    # 使用传入的app实例来加载任务和启动调度器
        reload_tasks(app)
        if not scheduler.running:
         scheduler.start()

    # 确保在Flask应用关闭时关闭调度器
    @app.teardown_appcontext
    def shutdown_scheduler(exception=None):
        if scheduler.running:
            scheduler.shutdown()
