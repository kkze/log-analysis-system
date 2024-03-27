# backend/app/__init__.py

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import JWTManager
from flask_migrate import Migrate
import os
from dotenv import load_dotenv
# 加载环境变量
load_dotenv()

# 在函数外部初始化 Flask 扩展
db = SQLAlchemy()
migrate = None
jwt = JWTManager()

def create_app():
    app = Flask(__name__)

    # 应用配置
    app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL')
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['JWT_SECRET_KEY'] = os.getenv('JWT_SECRET_KEY')

    # 将应用实例与 Flask 扩展绑定
    db.init_app(app)
    jwt.init_app(app)

    # 初始化并绑定 Flask-Migrate
    migrate = Migrate(app, db, directory='backend/migrations')
    print('成功初始化并绑定 Flask-Migrate')

    # 在此处导入TokenBlacklist模型
    from .models import TokenBlacklist

    @jwt.token_in_blocklist_loader
    def check_if_token_in_blacklist(jwt_header, jwt_payload):
        jti = jwt_payload["jti"]
        token = TokenBlacklist.query.filter_by(jti=jti).first()
        return token is not None


    # 使用相对导入来导入 configure_routes 函数
    from .routes import configure_routes
    configure_routes(app)
    print('成功注册路由')

    return app
