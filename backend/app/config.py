# backend/app/config.py
import os
from dotenv import load_dotenv

# 加载环境变量
load_dotenv()

class Config:
    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URL')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    JWT_SECRET_KEY = os.getenv('JWT_SECRET_KEY')
    CORS_ORIGINS = ["http://localhost:3333"]
