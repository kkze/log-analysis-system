import random
from datetime import datetime, timedelta

import pytz

# 日志文件名格式
date = datetime.now(pytz.timezone('Asia/Shanghai')) - timedelta(days=1)  # T+1日志
filename = date.strftime("web.log.%Y.%m.%d.log")

# 可能的IP地址、请求路径、HTTP方法和状态码
ips = ["127.0.0.1", "192.168.1.1", "10.0.0.1"]
paths = ["/index.html", "/submit-form", "/style.css", "/image.png", "/script.js"]
methods = ["GET", "POST"]
status_codes = [200, 404, 500]

# 生成指定数量的日志条目
def generate_log_entries(num_entries=100):
    with open(filename, 'w') as f:
        for _ in range(num_entries):
            ip = random.choice(ips)
            path = random.choice(paths)
            method = random.choice(methods)
            status = random.choice(status_codes)
            # 构造日志时间
            log_time = (date + timedelta(minutes=random.randint(1, 1440))).strftime('%d/%b/%Y:%H:%M:%S +0000')
            # 构造日志条目
            log_entry = f"{ip} - - [{log_time}] \"{method} {path} HTTP/1.1\" {status}\n"
            f.write(log_entry)

# 调用函数生成日志
generate_log_entries(100)  # 生成100条日志条目

print(f"Generated log file: {filename}")
