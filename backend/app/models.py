from . import db
import datetime
from flask_sqlalchemy import SQLAlchemy
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
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.datetime.utcnow)

    def __init__(self, jti):
        self.jti = jti

# 任务表
class Task(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    status = db.Column(db.String(20), nullable=False, default='stopped')  # 任务状态，默认为停止状态
    schedule = db.Column(db.String(100), nullable=False)  # 任务调度表达式或其他格式

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "status": self.status,
            "schedule": self.schedule
        }