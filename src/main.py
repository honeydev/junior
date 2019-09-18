"""Модуль запуска сервера."""

from flask import Flask
from flask_sqlalchemy import SQLAlchemy

from src.settings import DevelopConfig

from src.user.views import user_bp
from src.views import index_bp

# App init
app = Flask(__name__,)
app.config.from_object(DevelopConfig)

# BluePrint init
app.register_blueprint(index_bp)
app.register_blueprint(user_bp)

# DataBase init
db = SQLAlchemy(app=app)
db.init_app(app=app)

if __name__ == '__main__':
    app.run()
