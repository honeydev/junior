from src.main import db


class User(db.Model):
    __tablename__ = 'users'
    __table_args__ = {'extend_existing': True}
    extend_existing = True
    id = db.Column(db.Integer, primary_key=True)
    login = db.Column(db.String(), )
    password = db.Column(db.String(), )
    email = db.Column(db.String(), )
    firstname = db.Column(db.String(), )
    middlename = db.Column(db.String(), )
    lastname = db.Column(db.String(), )

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

    def __repr__(self):
        return '<id {}>'.format(self.id)
