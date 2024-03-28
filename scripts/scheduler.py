from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.cron import CronTrigger
import os
import sys

# 确保可以导入其他脚本
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'backend'))
from app import create_app
from log_parser import main as parse_logs

app = create_app()
scheduler = BackgroundScheduler()

# 配置日志解析任务
@scheduler.scheduled_job(CronTrigger(hour='12', minute='12'))  # 每天午夜执行
def scheduled_log_parse():
    with app.app_context():
        parse_logs()

# 测试代码
# @scheduler.scheduled_job(CronTrigger(second='0'))  # 每分钟执行一次
# def scheduled_log_parse():
#     with app.app_context():
#         parse_logs()

if __name__ == '__main__':
    scheduler.start()

    # 为了防止脚本退出，启动一个无限循环
    try:
        while True:
            pass
    except (KeyboardInterrupt, SystemExit):
        scheduler.shutdown()
