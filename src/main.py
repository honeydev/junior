"""Модуль запуска сервера."""

import os

from flask import Flask
from flask_admin.contrib.sqla import ModelView
from flask_dance.contrib.github import make_github_blueprint
from flask_mail import Mail
from flask_sessionstore import SqlAlchemySessionInterface

from src import user
from src.admin_forms import QAWYSIWYG
from src.commands import create_admin_user, load_chapters_questions
from src.extensions import admin, bcrypt, db, migrate, sess
from src.qa.models import Answer, Question
from src.qa.views import bp as qa_bp
from src.settings import DevelopConfig
from src.test_cases import TestAnswer, TestCase, TestQuestion, TestQuestionUserRelation
from src.test_cases.views import bp as test_cases_bp
from src.user import User
from src.user.auth import auth_hook
from src.views import bp as index_bp


def create_app(config=DevelopConfig):
    """App factory."""
    app = Flask(
        __name__.split('.')[0],
        static_url_path='/static',
        static_folder=f'{config.PROJECT_PATH}/src/static'
    )
    app.url_map.strict_slashes = False
    app.config.from_object(config)
    register_extensions(app)
    register_blueprints(app)
    register_shellcontext(app)
    register_adminpanel(app)
    register_sessions(app)
    register_github_oauth(app)
    register_before_hooks(app)
    register_commands(app)
    register_mail_settings(app)
    register_secret(app)
    return app


def register_extensions(app):
    """Flask extensions."""
    bcrypt.init_app(app)
    db.init_app(app)
    migrate.init_app(app, db)
    admin.init_app(app)


def register_adminpanel(app):
    app.config['FLASK_ADMIN_SWATCH'] = 'darkly'
    admin.add_view(ModelView(User, db.session))
    admin.add_view(QAWYSIWYG(TestCase, db.session))
    admin.add_view(QAWYSIWYG(TestQuestion, db.session))
    admin.add_view(QAWYSIWYG(TestAnswer, db.session))
    admin.add_view(QAWYSIWYG(Answer, db.session))
    admin.add_view(QAWYSIWYG(Question, db.session))
    admin.add_view(QAWYSIWYG(TestQuestionUserRelation, db.session))


def register_sessions(app):
    app.config['SESSION_TYPE'] = 'sqlalchemy'
    app.config['SESSION_SQLALCHEMY'] = db
    SqlAlchemySessionInterface(app, db, 'flask_sessions', 'key_')
    sess.init_app(app)
    return app


def register_blueprints(app):
    app.register_blueprint(user.views.bp)
    app.register_blueprint(index_bp)
    app.register_blueprint(qa_bp)
    app.register_blueprint(test_cases_bp)


def register_shellcontext(app):
    """Register shell context objects."""

    def shell_context():
        """Shell context objects."""
        return {
            'db': db,
            'User': user.models.User,
        }

    app.shell_context_processor(shell_context)


def register_github_oauth(app):
    app.config["GITHUB_OAUTH_CLIENT_ID"] = os.environ.get("GITHUB_OAUTH_CLIENT_ID")
    app.config["GITHUB_OAUTH_CLIENT_SECRET"] = os.environ.get("GITHUB_OAUTH_CLIENT_SECRET")
    github_bp = make_github_blueprint()
    app.register_blueprint(github_bp, url_prefix="/login")


def register_before_hooks(app):
    app.before_request(auth_hook)


def register_commands(app):
    app.cli.add_command(load_chapters_questions)
    app.cli.add_command(create_admin_user)


def register_mail_settings(app):
    mail = Mail(app)
    app.config["MAIL_SERVER"] = os.environ.get("MAIL_SERVER")
    app.config["MAIL_PORT"] = int(os.environ.get("MAIL_PORT"))
    app.config["MAIL_USE_TLS"] = os.environ.get("MAIL_USE_TLS")
    app.config["MAIL_USERNAME"] = os.environ.get("MAIL_USERNAME")
    app.config["MAIL_PASSWORD"] = os.environ.get("MAIL_PASSWORD")
    app.config["ADMINS"] = os.environ.get("ADMINS")
    return mail


def register_secret(app):
    app.config["SECRET_KEY"] = os.environ.get("SECRET_KEY")
