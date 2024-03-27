# Log parsing script 
from app import db
from app.models import LogEntry
from app.utils import parse_log_line

def store_log_data(filename):
    with open(filename, 'r') as file:
        for line in file:                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                        
            data = parse_log_line(line)
            if data:
                log_entry = LogEntry(
                    ip_address=data['ip'],
                    date=data['date'],
                    path=data['path'],
                    http_code=int(data['code']),
                    is_invalid=False  # 这里可以添加逻辑来判断请求是否无效
                )
                db.session.add(log_entry)
        db.session.commit()

# 假设日志文件位于项目根目录
log_file_name = 'web.log'  # 这里应该替换成实际的日志文件名
store_log_data(log_file_name)
