# Utility functions go here 
import re
from datetime import datetime

# 日志行的正则表达式
log_line_re = re.compile(r'(?P<ip>\S+) - - \[(?P<date>\S+ \S+)\] "(?P<method>\S+) (?P<path>\S+) \S+" (?P<code>\d+)')

# 解析日志行
def parse_log_line(line):
    match = log_line_re.match(line)
    if match:
        data = match.groupdict()
        # 转换日期格式
        data['date'] = datetime.strptime(data['date'], '%d/%b/%Y:%H:%M:%S %z').date()
        return data
    return None
