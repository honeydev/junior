"""Модуль запуска сервера."""

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from junior import settings
from junior.user.views import bp
from junior.app.views import index_bp

db = SQLAlchemy()

app = Flask(__name__,)
app.register_blueprint(index_bp)
app.register_blueprint(bp)
app.config['SQLALCHEMY_DATABASE_URI'] = settings.DATABASE_URL
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db.init_app(app=app)


if __name__ == '__main__':
    app.run()
