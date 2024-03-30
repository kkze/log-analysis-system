from flask import jsonify, current_app
from .models import db
from datetime import datetime, timedelta
from apscheduler.triggers.cron import CronTrigger
from apscheduler.triggers.date import DateTrigger

def perform_db_operation(db_operation, success_message, failure_message):
    try:
        db_operation()  # 执行数据库操作
        db.session.commit()  # 提交更改
        return jsonify({"message": success_message}), 200
    except Exception as e:
        db.session.rollback()  # 回滚更改
        current_app.logger.error(f"{failure_message}: {e}")  # 记录错误日志
        return jsonify({"error": failure_message, "detail": str(e)}), 500


def generate_scheduler_params(task_type, execute_type, schedule=None, next_run=None):
    """
    根据任务类型和执行计划生成APScheduler的调度参数。

    :param task_type: 任务的类型，'single' 或 'repeat'。
    :param execute_type: 执行类型，'immediate' 或 'scheduled'。
    :param schedule: 对于重复任务，'daily', 'hourly', 'monthly', 'minutely' 的周期。
    :param next_run: 对于计划执行的任务，起始执行时间（datetime对象）。
    :return: APScheduler的调度参数字典。
    """
    params = {}
    if task_type == 'single':
        if execute_type == 'immediate':
            # 立即执行的单次任务，使用当前时间
            params['trigger'] = DateTrigger(run_date=datetime.now() + timedelta(seconds=10))  # 延迟10秒执行，以防立即执行
        elif execute_type == 'scheduled':
            # 计划执行的单次任务
            params['trigger'] = DateTrigger(run_date=next_run)
    elif task_type == 'repeat':
        cron_expression = None
        if schedule == 'daily':
            cron_expression = CronTrigger(day='*', hour=next_run.hour, minute=next_run.minute)
        elif schedule == 'hourly':
            cron_expression = CronTrigger(hour='*', minute=next_run.minute)
        elif schedule == 'monthly':
            cron_expression = CronTrigger(day=next_run.day, hour=next_run.hour, minute=next_run.minute)
        elif schedule == 'minutely':
            cron_expression = CronTrigger(minute='*')
        
        if execute_type == 'immediate':
            # 立即执行的重复任务
            params['trigger'] = cron_expression
        elif execute_type == 'scheduled':
            # 计划执行的重复任务
            params['trigger'] = cron_expression
            params['start_date'] = next_run
    
    return params
