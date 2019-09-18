"""Модуль запуска сервера."""

from flask import Flask
from flask_migrate import Migrate, MigrateCommand
from flask_script import Manager
from flask_sqlalchemy import SQLAlchemy

from .settings import DevelopConfig

from .user.views import user_bp
from .views import index_bp

# App init
app = Flask(__name__,)
app.config.from_object(DevelopConfig)

# BluePrint init
app.register_blueprint(index_bp)
app.register_blueprint(user_bp)

# DataBase init
db = SQLAlchemy(app=app)
db.init_app(app=app)
migrate = Migrate()

from .user.models import *

migrate.init_app(app, db)
manager = Manager(app)
manager.add_command('db', MigrateCommand)

if __name__ == '__main__':
    manager.run()
