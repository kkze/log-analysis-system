# backend/app/__init__.py
from dotenv import load_dotenv
from flask import Flask
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
from .route_error_handlers import register_error_handlers
from .route_blueprints import all_blueprints
from .config import Config  # 导入应用配置
from .extensions import db, jwt  # 导入数据库和JWT扩展
from flask_migrate import Migrate  # 导入数据库迁移工具
from .scheduler import init_scheduler  # 导入调度器初始化函数
from .jwt_config import configure_jwt  # 导入JWT配置函数
# 加载环境变量
load_dotenv()

def create_app():
    
    # 创建Flask应用实例
    app = Flask(__name__)
    # 从Config类加载配置
    app.config.from_object(Config)
    
    # 初始化CORS支持，允许跨域请求
    CORS(app, resources={r"/*": {"origins": Config.CORS_ORIGINS}}, supports_credentials=True)
    
    # 初始化数据库扩展
    db.init_app(app)
    # 初始化JWT扩展
    jwt.init_app(app)
    
    with app.app_context():
        db.create_all()  # 创建或更新数据库表结构

    # 配置和初始化数据库迁移工具
    Migrate(app, db)
    
    # 调用JWT配置函数，设置JWT相关的回调函数，如token_in_blocklist_loader
    configure_jwt(jwt)
    
    # 初始化调度器，加载并启动预定的后台任务
    init_scheduler(app)
    
    # 注册错误处理器
    register_error_handlers(app)

    # 循环导入并注册蓝图路由
    for blueprint, prefix in all_blueprints:
        app.register_blueprint(blueprint, url_prefix=prefix)
    
    return app
