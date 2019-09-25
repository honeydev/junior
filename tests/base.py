from flask_testing import TestCase

from src.extensions import db
from src.main import create_app
from src.settings import TestConfig


class BaseTest(TestCase):

    TESTING = True
    BASE_APP = create_app(TestConfig)

    def setUp(self):
        db.init_app(self.app)
        db.create_all()

    def create_app(self):
        self.BASE_APP.config['TESTING'] = True
        # Default port is 5000
        self.BASE_APP.config['LIVESERVER_PORT'] = 8943
        # Default timeout is 5 seconds
        self.BASE_APP.config['LIVESERVER_TIMEOUT'] = 10
        return self.BASE_APP

    def tearDown(self):
        db.session.remove()
        db.drop_all()
