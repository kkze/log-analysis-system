# Routes go here 
# routes.py
from flask import request, jsonify
from flask_jwt_extended import create_access_token, get_jwt, get_jwt_identity, jwt_required
from .models import LogEntry, TokenBlacklist, User, db  # 使用相对导入

def configure_routes(app):
     
    # 注册
    @app.route('/api/auth/register', methods=['POST'])
    def register():
        if not request.is_json:
            return jsonify({"msg": "Missing JSON in request"}), 400

        username = request.json.get('username', None)
        password = request.json.get('password', None)
        if not username or not password:
            return jsonify({"msg": "Missing username or password"}), 400

        if User.query.filter_by(username=username).first():
            return jsonify({"msg": "Username already exists"}), 400

        user = User(username=username)
        user.set_password(password)
        db.session.add(user)
        db.session.commit()

        return jsonify({"msg": "User registered successfully"}), 201
     
     
    #登录
    @app.route('/api/auth/login', methods=['POST'])
    def login():
        if not request.is_json:
            return jsonify({"msg": "Missing JSON in request"}), 400
    
        username = request.json.get('username', None)
        password = request.json.get('password', None)
        if not username or not password:
            return jsonify({"msg": "Missing username or password"}), 400
    
        user = User.query.filter_by(username=username).first()
        if user is None or not user.check_password(password):
            return jsonify({"msg": "Bad username or password"}), 401
    
        access_token = create_access_token(identity=username)
        return jsonify(access_token=access_token), 200
    
    # 登出
    @app.route('/api/auth/logout', methods=['GET'])
    @jwt_required()
    def logout():
        jti = get_jwt()['jti']
        db.session.add(TokenBlacklist(jti=jti))
        db.session.commit()
        return jsonify(msg="Successfully logged out"), 200

    # 获取日志文件列表
    @app.route('/api/logs', methods=['GET'])
    @jwt_required()
    def get_logs():
        current_user = get_jwt_identity()
        if not current_user:
            return jsonify({"msg": "Unauthorized"}), 401

        query = LogEntry.query

        # 获取查询参数
        date = request.args.get('date', type=str)
        ip = request.args.get('ip', type=str)
        path = request.args.get('path', type=str)
        http_code = request.args.get('http_code', type=int)

        # 应用筛选条件
        if date:
            query = query.filter(LogEntry.date == date)
        if ip:
            query = query.filter(LogEntry.ip_address.like(f"%{ip}%"))
        if path:
            query = query.filter(LogEntry.path.like(f"%{path}%"))
        if http_code:
            query = query.filter(LogEntry.http_code == http_code)

        logs = query.all()

        return jsonify([log.to_dict() for log in logs])

    # 获取日志详情
    @app.route('/api/logs/<int:id>', methods=['GET'])
    @jwt_required()
    def get_log(id):
        current_user = get_jwt_identity()
        if not current_user:
            return jsonify({"msg": "Unauthorized"}), 401

        log = LogEntry.query.get(id)
        if not log:
            return jsonify({"error": "Log not found"}), 404

        return jsonify(log.to_dict())
    
    # 创建日志条目
    @app.route('/api/logs', methods=['POST'])
    @jwt_required()
    def create_log():
        current_user = get_jwt_identity()
        if not current_user:
            return jsonify({"msg": "Unauthorized"}), 401

        data = request.json
        if not data:
            return jsonify({"msg": "No data provided"}), 400

        date = data.get('date')
        ip_address = data.get('ip_address')
        path = data.get('path')
        http_code = data.get('http_code')
        is_invalid = data.get('is_invalid')

        if not all([date, ip_address, path, http_code]):
            return jsonify({"msg": "Missing required fields"}), 400

        log = LogEntry(date=date, ip_address=ip_address, path=path, http_code=http_code, is_invalid=is_invalid)
        db.session.add(log)
        db.session.commit()

        return jsonify({"msg": "Log created successfully"}), 201
