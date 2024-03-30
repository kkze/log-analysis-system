from flask import jsonify

def not_found(error):
    """处理 404 错误"""
    return jsonify({"error": "资源未找到", "description": str(error)}), 404

def bad_request(error):
    """处理 400 错误"""
    return jsonify({"error": "错误的请求", "description": str(error)}), 400

def internal_server_error(error):
    """处理 500 错误"""
    return jsonify({"error": "内部服务器错误", "description": str(error)}), 500

def method_not_allowed(error):
    """处理 405 错误"""
    return jsonify({"error": "方法不被允许", "description": str(error)}), 405

def register_error_handlers(app):
    """
    注册全局错误处理器到 Flask 应用。
    """
    app.register_error_handler(400, bad_request)
    app.register_error_handler(404, not_found)
    app.register_error_handler(500, internal_server_error)
    app.register_error_handler(405, method_not_allowed)
