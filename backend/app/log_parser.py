import re
import os
from datetime import datetime, timedelta
import zipfile
from pathlib import Path
from flask import current_app
from .models import LogEntry, db  # 更新导入路径

# 日志文件名格式：web.log.YYYY.MM.DD.log
def get_log_filename():
    date = (datetime.now() - timedelta(days=1)).strftime("%Y.%m.%d")
    return f"web.log.{date}.log"

# 解析日志行
def parse_log_line(line):
    log_pattern = re.compile(
        r'(?P<ip>\S+) - - \[(?P<datetime>[^\]]+)\] "(?P<request>[^"]+)" (?P<status>\d+)'
    )
    match = log_pattern.match(line)
    if not match:
        return None
    data = match.groupdict()

    # 解析请求部分
    request_parts = data['request'].split()
    if len(request_parts) != 3:
        return None
    method, path, _ = request_parts

    # 识别无效请求
    is_invalid = path.endswith(('.js', '.css', '.jpg', '.png', '.gif')) or data['status'].startswith(('4', '5'))

    return {
        'ip': data['ip'],
        'datetime': data['datetime'],
        'path': path,
        'status': int(data['status']),
        'is_invalid': is_invalid
    }

# 读取并解析日志文件
def parse_log_file(filename):
    parsed_lines = []
    with open(filename, 'r') as file:
        for line in file:
            parsed_line = parse_log_line(line)
            if parsed_line:
                parsed_lines.append(parsed_line)
    return parsed_lines

# 保存解析的日志到数据库
def save_parsed_data_to_db(parsed_data):
    for data in parsed_data:
        log_entry = LogEntry(
            ip_address=data['ip'],
            date=datetime.strptime(data['datetime'], '%d/%b/%Y:%H:%M:%S %z').date(),
            path=data['path'],
            http_code=data['status'],
            is_invalid=data['is_invalid']
        )
        db.session.add(log_entry)
    db.session.commit()

# 日志备份
def backup_log_file(log_filename):
    # 定义备份目录路径
    backup_dir = Path('logbackup')
    # 确保备份目录存在
    backup_dir.mkdir(exist_ok=True)
    
    # 构建备份文件的完整路径
    zip_filename = backup_dir / f"{log_filename}.zip"
    
    # 创建ZIP文件并添加日志文件
    with zipfile.ZipFile(zip_filename, 'w', zipfile.ZIP_DEFLATED) as zipf:
        zipf.write(log_filename, arcname=Path(log_filename).name)
    print(f"Backup of {log_filename} created at {zip_filename}")


# 主逻辑
def main():
    log_filename = get_log_filename()
    if not os.path.exists(log_filename):
        print(f"Log file {log_filename} does not exist.")
    else:
        parsed_data = parse_log_file(log_filename)
        save_parsed_data_to_db(parsed_data)
        backup_log_file(log_filename)
        print(f"Successfully parsed and saved {len(parsed_data)} lines to database.")

if __name__ == "__main__":
        main()
