from flask import jsonify, current_app
import pytz
from .models import db
from datetime import datetime, timedelta
from apscheduler.triggers.cron import CronTrigger
from apscheduler.triggers.date import DateTrigger

def perform_db_operation(db_operation, success_message, failure_message):
    try:
        db_operation()  # 执行数据库操作
        db.session.commit()  # 提交更改
        return jsonify({"message": success_message})
    except Exception as e:
        db.session.rollback()  # 回滚更改
        current_app.logger.error(f"{failure_message}: {e}")  # 记录错误日志
        return jsonify({"error": failure_message, "detail": str(e)}), 500
    
from datetime import datetime, timedelta
from apscheduler.triggers.date import DateTrigger
from apscheduler.triggers.cron import CronTrigger
import pytz

def generate_scheduler_params(task_type, execute_type, schedule=None, start_time=None, day_of_week=None):
    """
    生成APScheduler的调度参数，考虑到任务类型、执行计划、以及任务的具体调度需求。
    现在增加了一个新的逻辑：如果开始时间小于当前时间，那么开始时间将被设置为当前时间加1秒。
    """
    tz = pytz.timezone('Asia/Shanghai')  # 定义时区
    now = datetime.now(tz)
    params = {}
    print(f"start_time:{start_time}")
    if task_type == 'single':
        if execute_type == 'immediate':
            # 立即执行的单次任务，延迟1秒以避免立即执行的问题
            params['trigger'] = DateTrigger(run_date=now + timedelta(seconds=1))
        elif execute_type == 'scheduled' and start_time:
            # 计划执行的单次任务，使用更新后的开始时间
            local_time =start_time.replace(tzinfo=tz)
            print(f"tz:{local_time}")
            params['trigger'] = DateTrigger(run_date=local_time)
    elif task_type == 'repeat':
        cron_fields = {
            'second': start_time.second if start_time else '0',
            'minute': start_time.minute if start_time and schedule != 'minutely' else '*',
            'hour': start_time.hour if start_time and schedule in ['daily', 'weekly'] else '*',
            'day': start_time.day if start_time and schedule == 'monthly' else '*',
            'month': '*',
            'day_of_week': day_of_week if schedule == 'weekly' else '*',
            'timezone': tz
        }
        params['trigger'] = CronTrigger(**cron_fields)

        if execute_type == 'scheduled' and start_time:
            # 如果任务计划在将来某个时间点开始执行，设置start_date为更新后的开始时间
            params['start_date'] = start_time

    return params

def repeat_to_cron(schedule, start_time=None, day_of_week=None):
    """
    将自定义的重复模式转换为精确到秒的CRON表达式。

    :param schedule: 重复模式，可选值 'daily', 'hourly', 'monthly', 'minutely', 'weekly'。
    :param start_time: 任务的起始执行时间（datetime对象），仅在非'minutely'模式下使用。
    :param day_of_week: 在'weekly'模式下，指定星期几执行，值为0到6（0表示周日，6表示周六）。
    :return: 对应的CRON表达式。
    """
    # CRON表达式的秒、分钟、小时、日、月、星期部分默认为"*"
    second = "*"
    minute = "*"
    hour = "*"
    day = "*"
    month = "*"
    day_of_week_str = "*"

    # 如果提供了start_time，更新秒、分钟、小时的值
    if start_time:
        second = start_time.second
        minute = start_time.minute
        hour = start_time.hour
        day = start_time.day
        month = start_time.month
        day_of_week_str = day_of_week
    # 根据不同的重复模式调整CRON表达式的值
    if schedule == 'minutely':
        # 每分钟执行，只需指定秒
        cron_exp = f'{second} * * * * *'
    elif schedule == 'hourly':
        # 每小时执行，指定秒和分钟
        cron_exp = f'{second} {minute} * * * *'
    elif schedule == 'daily':
        # 每天执行，指定秒、分钟和小时
        cron_exp = f'{second} {minute} {hour} * * *'
    elif schedule == 'monthly' and start_time:
        # 每月执行，指定秒、分钟、小时和日
        day = start_time.day
        cron_exp = f'{second} {minute} {hour} {day} * *'
    elif schedule == 'weekly' and day_of_week is not None:
        # 每周执行，指定秒、分钟、小时和星期几
        day_of_week_str = str(day_of_week)
        cron_exp = f'{second} {minute} {hour} * * {day_of_week_str}'
    else:
        raise ValueError(f"Unsupported schedule: {schedule}")

    return cron_exp