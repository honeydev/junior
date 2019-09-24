from flask_migrate import Migrate, MigrateCommand
from flask_script import Manager

from app import app
from src.user.models import *
from src.faq.models import Question, Answer

migrate = Migrate(app, db)

manager = Manager(app)

manager.add_command('db', MigrateCommand)

if __name__ == '__main__':
    manager.run()
