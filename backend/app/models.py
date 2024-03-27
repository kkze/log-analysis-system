# Models go here 
from . import db

class LogEntry(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    ip_address = db.Column(db.String(255), nullable=False)
    date = db.Column(db.Date, nullable=False)
    path = db.Column(db.String(255), nullable=False)
    http_code = db.Column(db.Integer, nullable=False)
    is_invalid = db.Column(db.Boolean, default=False, nullable=False)
