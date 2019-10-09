from flask_bcrypt import check_password_hash, generate_password_hash

from src.extensions import db


class User(db.Model):  # noqa: WPS230
    __tablename__ = 'users'
    __table_args__ = {'extend_existing': True}

    def __init__(  # noqa: S107 WPS211
            self,
            login: str,
            email: str,
            password: str = '',
            firstname: str = '',
            middlename: str = '',
            lastname: str = '',
            is_oauth: bool = False,
            is_superuser: bool = False,
    ):
        self.login = login
        self.password = password
        self.email = email
        self.firstname = firstname
        self.middlename = middlename
        self.lastname = lastname
        self.is_oauth = is_oauth
        self.is_superuser = is_superuser

    id = db.Column(db.Integer, primary_key=True)  # noqa: A003
    login = db.Column(db.String(), unique=True)
    password = db.Column(db.String())
    email = db.Column(db.String(), unique=True)
    firstname = db.Column(db.String(), nullable=True)
    middlename = db.Column(db.String(), nullable=True)
    lastname = db.Column(db.String(), nullable=True)
    is_oauth = db.Column(db.Boolean, default=False, nullable=False)
    is_superuser = db.Column(db.Boolean, default=False, nullable=False)
    db.relationship(  # noqa: WPS604
        'User', backref='users', lazy='dynamic',
    )

    def __repr__(self):
        return '<id {0}>'.format(self.id)

    @classmethod
    def hash_password(cls, password: str):
        return generate_password_hash(password=password)

    def check_password(self, password):
        return check_password_hash(self.password, password)
