from flask import request, jsonify, Blueprint
from flask_cors import cross_origin
from flask_jwt_extended import create_access_token, get_jwt, jwt_required
from .models import TokenBlacklist, User, db  # 使用相对导入
# 定义Blueprint
bp_auth = Blueprint('auth', __name__)


# 注册
@bp_auth.route('/register', methods=['POST'])
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
@bp_auth.route('/login', methods=['POST'])
@cross_origin()
def login():
    if not request.is_json:
        return jsonify({"msg": "Missing JSON in request"}), 400
    print(request.json)
    username = request.json.get('username', None)
    password = request.json.get('password', None)
    if not username or not password:
        return jsonify({"msg": "Missing username or password"}), 400

    user = User.query.filter_by(username=username).first()
    if user is None or not user.check_password(password):
        return jsonify({"msg": "Bad username or password"}), 401

    access_token = create_access_token(identity=username)
    return jsonify(token=access_token), 200

# 登出
@bp_auth.route('/logout', methods=['GET'])
@jwt_required()
def logout():
    jti = get_jwt()['jti']
    db.session.add(TokenBlacklist(jti=jti))
    db.session.commit()
    return jsonify(msg="Successfully logged out"), 200
