from flask_bcrypt import check_password_hash, generate_password_hash

from src.extensions import db


class User(db.Model, ):
    __tablename__ = 'users'
    __table_args__ = {'extend_existing': True}

    def __init__(
            self, login, password, email,
            firstname, middlename, lastname
    ):
        self.login = login
        self.password = password
        self.email = email
        self.firstname = firstname
        self.middlename = middlename
        self.lastname = lastname

    id = db.Column(db.Integer, primary_key=True)
    login = db.Column(db.String(), unique=True)
    password = db.Column(db.String(), )
    email = db.Column(db.String(), unique=True)
    firstname = db.Column(db.String(), nullable=True)
    middlename = db.Column(db.String(), nullable=True)
    lastname = db.Column(db.String(), nullable=True)

    def __repr__(self):
        return '<id {}>'.format(self.id)

    @staticmethod
    def hash_password(password: str):
        return generate_password_hash(password=password)

    def check_password(self, password):
        return check_password_hash(self.password, password)
