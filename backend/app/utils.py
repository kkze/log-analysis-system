from flask import jsonify, current_app
from .models import db

def perform_db_operation(db_operation, success_message, failure_message):
    try:
        db_operation()  # 执行数据库操作
        db.session.commit()  # 提交更改
        return jsonify({"message": success_message}), 200
    except Exception as e:
        db.session.rollback()  # 回滚更改
        current_app.logger.error(f"{failure_message}: {e}")  # 记录错误日志
        return jsonify({"error": failure_message, "detail": str(e)}), 500
