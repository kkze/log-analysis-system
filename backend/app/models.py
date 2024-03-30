from datetime import datetime, timezone

import pytz
from .extensions import db
from werkzeug.security import generate_password_hash, check_password_hash

# 日志表
class LogEntry(db.Model):
    __tablename__ = 'log_entries'  # 指定表名
    id = db.Column(db.Integer, primary_key=True)
    ip_address = db.Column(db.String(255))
    date = db.Column(db.Date)
    path = db.Column(db.String(255))
    http_code = db.Column(db.Integer)
    is_invalid = db.Column(db.Boolean, default=False)

    def __repr__(self):
        return '<LogEntry %r>' % self.ip_address
    
    def to_dict(self):
        return {
        'id': self.id,
        'ip_address': self.ip_address,
        'date': self.date.isoformat(),
        'path': self.path,
        'http_code': self.http_code,
        'is_invalid': self.is_invalid
        }

# 用户表
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True)
    password_hash = db.Column(db.String(1024))  # 更改为1024或根据需要调整

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

# 黑名单，用于从服务端控制用户登出
class TokenBlacklist(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    jti = db.Column(db.String(36), nullable=False, unique=True)
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.now(timezone.utc))

    def __init__(self, jti):
        self.jti = jti

# 任务表
class ScheduledTask(db.Model):
    __tablename__ = 'scheduled_tasks'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    task_type = db.Column(db.String(255), nullable=False)  # 表示任务类型的字段
    status = db.Column(db.String(20),  nullable=True, default='stopped')  # 任务的状态
    schedule = db.Column(db.String(100),  nullable=True)  # `task_type`为`repeat`时需指定，可选值有`daily`（每天），`hourly`（每小时），`minutely`（每分钟），`monthly`（每月），`weekly`（每周）
    last_run = db.Column(db.DateTime)  # 最后一次运行时间
    next_run = db.Column(db.DateTime)  # 下一次运行时间
    start_time = db.Column(db.DateTime, default=datetime.now(pytz.timezone('Asia/Shanghai'))) #开始运行的时间
    execute_type = db.Column(db.String(20), nullable=False, default='immediate')  # 可为`immediate`（立即执行）或`scheduled`（计划执行）
    day_of_week = db.Column(db.String(20), nullable=True)  # 对于每周重复任务，指定星期几执行，值为0到6（0表示周日，6表示周六）
    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'task_type': self.task_type,
            'status': self.status,
            'execute_type': self.execute_type,
            'schedule': self.schedule if self.schedule else None,
            'last_run': self.last_run.isoformat() if self.last_run else None,
            'next_run': self.next_run.isoformat() if self.next_run else None,
            'start_time': self.start_time.isoformat() if self.start_time else None,
        }

# 任务执行日志表
class TaskExecutionLog(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    task_id = db.Column(db.Integer, db.ForeignKey('scheduled_tasks.id'), nullable=False)
    executed_at = db.Column(db.DateTime, default=datetime.now(pytz.timezone('Asia/Shanghai')))
    was_successful = db.Column(db.Boolean, default=True)
    message = db.Column(db.Text, nullable=True)

    def __init__(self, task_id, executed_at, was_successful, message=""):
        self.task_id = task_id
        self.executed_at = executed_at 
        self.was_successful = was_successful
        self.message = message